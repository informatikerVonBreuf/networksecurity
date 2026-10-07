"""Select a full pipeline using training CV and evaluate the winner on untouched test data."""

import json
import os
from dataclasses import asdict
from pathlib import Path

import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.artifact_entity import ModelTrainerArtifact
from networksecurity.utils.main_utils.utils import (
    evaluate_models,
    load_numpy_array_data,
    read_yaml_file,
    save_object,
)
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    """Persist a fitted inference bundle, comparable metrics and run metadata."""

    def __init__(self, model_trainer_config, data_transformation_artifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def track_mlflow(self, model, metrics, report):
        """Optionally log one experiment run to an explicitly configured tracking server."""
        if not os.getenv("MLFLOW_TRACKING_URI"):
            return
        import mlflow

        with mlflow.start_run():
            mlflow.log_params({"estimator": type(model).__name__, "random_state": 42})
            mlflow.log_metrics(metrics)
            mlflow.log_dict(report, "selection.json")
            mlflow.sklearn.log_model(model, "model")

    def train_model(self, X_train, y_train, x_test, y_test):
        """Fit fold-local preprocessing and select the highest mean CV F1."""
        estimators = {
            "Random Forest": RandomForestClassifier(random_state=42, n_jobs=1),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42),
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "AdaBoost": AdaBoostClassifier(random_state=42),
        }
        models = {
            name: Pipeline(
                [
                    ("preprocessor", DataTransformation.get_data_transformer_object()),
                    ("classifier", model),
                ]
            )
            for name, model in estimators.items()
        }
        params = {
            "Random Forest": {"classifier__n_estimators": [32, 64]},
            "Decision Tree": {"classifier__max_depth": [5, None]},
            "Gradient Boosting": {"classifier__n_estimators": [32, 64]},
            "Logistic Regression": {"classifier__C": [0.1, 1.0]},
            "AdaBoost": {"classifier__n_estimators": [32, 64]},
        }
        report = evaluate_models(X_train, y_train, models, params)
        name = max(report, key=report.get)
        best = models[name]
        if report[name] < self.model_trainer_config.expected_accuracy:
            raise ValueError("Cross-validation F1 is below the configured acceptance threshold.")
        train_metric = get_classification_score(y_train, best.predict(X_train))
        test_metric = get_classification_score(y_test, best.predict(x_test))
        features = [
            key
            for item in read_yaml_file("data_schema/schema.yaml")["columns"]
            for key in item
            if key != "Result"
        ]
        wrapper = NetworkModel(
            best.named_steps["preprocessor"], best.named_steps["classifier"], features
        )
        # Publish only after all evaluation and optional tracking operations have succeeded.
        metrics = {
            f"{split}_{key}": value
            for split, artifact in [("train", train_metric), ("test", test_metric)]
            for key, value in asdict(artifact).items()
        }
        self.track_mlflow(best, metrics, report)
        save_object(
            self.data_transformation_artifact.transformed_object_file_path, wrapper.preprocessor
        )
        save_object(self.model_trainer_config.trained_model_file_path, wrapper)
        model_dir = Path("final_model")
        model_dir.mkdir(exist_ok=True)
        staged = model_dir / "model.pending.pkl"
        save_object(staged, wrapper)
        staged.replace(model_dir / "model.pkl")
        summary = {
            "selected_model": name,
            "cv_f1": report,
            "metrics": metrics,
            "random_state": 42,
            "features": features,
            "label_mapping": {"-1": 0, "1": 1},
        }
        summary_path = Path(self.model_trainer_config.trained_model_file_path).with_suffix(".json")
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        (model_dir / "metrics.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return ModelTrainerArtifact(
            self.model_trainer_config.trained_model_file_path, train_metric, test_metric
        )

    def initiate_model_trainer(self):
        """Load prepared arrays and attach feature names for the fitted inference contract."""
        config = self.data_transformation_artifact
        train = load_numpy_array_data(config.transformed_train_file_path)
        test = load_numpy_array_data(config.transformed_test_file_path)
        features = [
            key
            for item in read_yaml_file("data_schema/schema.yaml")["columns"]
            for key in item
            if key != "Result"
        ]
        return self.train_model(
            pd.DataFrame(train[:, :-1], columns=features),
            train[:, -1],
            pd.DataFrame(test[:, :-1], columns=features),
            test[:, -1],
        )
