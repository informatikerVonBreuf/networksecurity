"""Tests du schéma, de l’évaluation et des prédictions."""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

import app
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig
from networksecurity.utils.main_utils.utils import evaluate_models, load_object, save_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


def validator():
    return DataValidation(None, DataValidationConfig(TrainingPipelineConfig()))


def test_schema_rejects_wrong_names_with_same_column_count():
    frame = pd.read_csv("Network_Data/phisingData.csv", nrows=5)
    assert validator().validate_number_of_columns(frame)
    frame = frame.rename(columns={"URL_Length": "incorrect"})
    with pytest.raises(ValueError, match="colonnes"):
        validator().validate_frame(frame)


def test_schema_rejects_missing_target_and_infinite_features():
    frame = pd.read_csv("Network_Data/phisingData.csv", nrows=5).astype(float)
    frame.loc[0, "Result"] = np.nan
    with pytest.raises(ValueError, match="Result"):
        validator().validate_frame(frame)
    frame.loc[0, "Result"] = -1
    frame.loc[0, "URL_Length"] = np.inf
    with pytest.raises(ValueError, match="infinie"):
        validator().validate_frame(frame)


def test_cv_uses_classification_f1_and_fits_preprocessing_inside_folds():
    # Prédire toujours zéro donne une accuracy positive, mais un F1 nul pour la classe 1.
    x = pd.DataFrame({"a": range(12)})
    y = np.array([0] * 9 + [1] * 3)
    models = {
        "baseline": Pipeline(
            [
                ("imputer", SimpleImputer()),
                ("classifier", DummyClassifier(strategy="most_frequent")),
            ]
        )
    }
    with patch.object(SimpleImputer, "fit", autospec=True, wraps=SimpleImputer.fit) as fit:
        # Garder le véritable ajustement tout en observant la taille des plis.
        fit.side_effect = lambda self, X, y=None: original_fit(self, X, y)
        report = evaluate_models(x, y, models, {"baseline": {}})
        sizes = [len(call.args[1]) for call in fit.call_args_list]
    assert report["baseline"] == 0.0
    assert sizes.count(8) == 3 and sizes.count(12) == 1


original_fit = SimpleImputer.fit


def bundle():
    frame = pd.DataFrame({"a": [0, 1, 2, 3], "b": [1, 0, 1, 0]})
    prep = SimpleImputer().fit(frame)
    model = DummyClassifier(strategy="most_frequent").fit(prep.transform(frame), [0, 1, 1, 1])
    return NetworkModel(prep, model, ["a", "b"]), frame


def test_bundle_survives_serialization_and_reorders_columns(tmp_path):
    model, frame = bundle()
    path = tmp_path / "model.pkl"
    save_object(path, model)
    restored = load_object(path)
    np.testing.assert_array_equal(restored.predict(frame), restored.predict(frame[["b", "a"]]))
    with pytest.raises(ValueError, match="colonnes"):
        restored.predict(frame.assign(Result=1))


def test_api_health_and_missing_model(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "MODEL_PATH", tmp_path / "missing.pkl")
    with TestClient(app.app) as client:
        assert client.get("/health").json()["model_available"] is False
        assert (
            client.post("/predict", files={"file": ("data.csv", "a,b\n1,2\n")}).status_code == 503
        )
        assert client.get("/train").status_code == 404


def test_api_predict_and_reject_invalid_csv(tmp_path, monkeypatch):
    model, frame = bundle()
    path = tmp_path / "model.pkl"
    save_object(path, model)
    monkeypatch.setattr(app, "MODEL_PATH", Path(path))
    with TestClient(app.app) as client:
        result = client.post("/predict", files={"file": ("data.csv", frame.to_csv(index=False))})
        assert result.status_code == 200 and "prediction" in result.text
        bad = client.post("/predict", files={"file": ("data.csv", "wrong\n1\n")})
        assert bad.status_code == 422


def test_duplicate_features_never_cross_holdout_boundary(tmp_path):
    from networksecurity.components.data_ingestion import DataIngestion
    from networksecurity.entity.config_entity import DataIngestionConfig

    config = DataIngestionConfig(TrainingPipelineConfig())
    config.training_file_path = str(tmp_path / "train.csv")
    config.testing_file_path = str(tmp_path / "test.csv")
    data = pd.DataFrame({"a": np.repeat(np.arange(30), 3), "Result": np.repeat([1, -1] * 15, 3)})
    DataIngestion(config).split_data_as_train_test(data)
    train = pd.read_csv(config.training_file_path)
    test = pd.read_csv(config.testing_file_path)
    assert not set(train.a) & set(test.a)
    assert len(train) + len(test) == len(data)


def test_duplicate_features_never_cross_cv_boundary():
    from sklearn.model_selection import StratifiedGroupKFold

    x = pd.DataFrame({"a": np.repeat(np.arange(30), 3)})
    y = np.repeat([0, 1] * 15, 3)
    models = {"baseline": Pipeline([("classifier", DummyClassifier())])}
    original_split = StratifiedGroupKFold.split
    observed = []

    def inspect_split(self, X, y, groups):
        for train, validation in original_split(self, X, y, groups):
            assert not set(X.iloc[train].a) & set(X.iloc[validation].a)
            observed.append(1)
            yield train, validation

    with patch.object(StratifiedGroupKFold, "split", inspect_split):
        evaluate_models(x, y, models, {"baseline": {}})
    assert len(observed) == 3
