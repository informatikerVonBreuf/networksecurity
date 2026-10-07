"""Typed contracts passed between stages and returned by training."""

from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """Raw training and holdout CSV paths."""

    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    """Schema acceptance, validated CSVs and an informational drift report."""

    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str | None
    invalid_test_file_path: str | None
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    """Raw numeric arrays and the preprocessing path populated by training."""

    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    """Positive-class F1, precision and recall."""

    f1_score: float
    precision_score: float
    recall_score: float


@dataclass
class ModelTrainerArtifact:
    """Saved inference bundle and train/holdout classification metrics."""

    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
