"""Objets échangés entre les étapes du pipeline."""

from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    """Chemins des CSV d’entraînement et de test."""

    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    """Résultat de validation, fichiers validés et chemin du rapport de distribution."""

    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str | None
    invalid_test_file_path: str | None
    drift_report_file_path: str


@dataclass
class DataTransformationArtifact:
    """Tableaux numériques et chemin du prétraitement ajusté pendant l’entraînement."""

    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    """F1, précision et rappel de la classe positive."""

    f1_score: float
    precision_score: float
    recall_score: float


@dataclass
class ModelTrainerArtifact:
    """Chemin du modèle et métriques sur l’entraînement et le test."""

    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
