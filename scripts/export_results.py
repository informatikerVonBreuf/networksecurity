"""Exporter les résultats mesurés et les caractéristiques du jeu de données."""

import hashlib
import json
import platform
from pathlib import Path

import pandas as pd
import sklearn


def main():
    """Écrire le rapport de résultats avec les versions utilisées et l’audit des partitions."""
    frame = pd.read_csv("Network_Data/phisingData.csv")
    summary = json.loads(Path("final_model/metrics.json").read_text(encoding="utf-8"))
    features = frame.drop(columns="Result")
    summary["dataset"] = {
        "rows": len(frame),
        "features": len(features.columns),
        "class_counts": {str(k): int(v) for k, v in frame.Result.value_counts().items()},
        "duplicate_rows": int(frame.duplicated().sum()),
        "unique_feature_groups": len(features.drop_duplicates()),
        "conflicting_feature_groups": int(
            (frame.groupby(list(features.columns))["Result"].nunique() > 1).sum()
        ),
        "missing_values": int(frame.isna().sum().sum()),
        "source_sha256": hashlib.sha256(
            Path("Network_Data/phisingData.csv").read_bytes()
        ).hexdigest(),
    }
    runs = [
        p
        for p in Path("Artifacts").iterdir()
        if (p / "model_trainer/trained_model/model.json").exists()
    ]
    latest = max(runs, key=lambda p: (p / "model_trainer/trained_model/model.json").stat().st_mtime)
    train = pd.read_csv(latest / "data_ingestion/ingested/train.csv")
    test = pd.read_csv(latest / "data_ingestion/ingested/test.csv")
    train_groups = set(pd.util.hash_pandas_object(train.drop(columns="Result"), index=False))
    test_groups = set(pd.util.hash_pandas_object(test.drop(columns="Result"), index=False))
    summary["partition_audit"] = {
        "train_rows": len(train),
        "test_rows": len(test),
        "train_groups": len(train_groups),
        "test_groups": len(test_groups),
        "overlapping_feature_groups": len(train_groups & test_groups),
    }
    summary["environment"] = {
        "python": platform.python_version(),
        "scikit_learn": sklearn.__version__,
        "pandas": pd.__version__,
    }
    summary["evaluation"] = {
        "split": "StratifiedGroupKFold: first of 5 folds as holdout",
        "selection": "3-fold StratifiedGroupKFold on training data",
        "group_key": "hash of all 30 features, excluding the target",
    }
    Path("docs/results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Rapport enregistré dans docs/results.json.")


if __name__ == "__main__":
    main()
