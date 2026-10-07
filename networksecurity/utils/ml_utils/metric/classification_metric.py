"""Binary classification metrics, with class 1 as the positive class."""

from sklearn.metrics import f1_score, precision_score, recall_score

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact


def get_classification_score(y_true, y_pred):
    """Return F1, precision and recall; undefined metrics are explicitly zero."""
    return ClassificationMetricArtifact(
        f1_score(y_true, y_pred, zero_division=0),
        precision_score(y_true, y_pred, zero_division=0),
        recall_score(y_true, y_pred, zero_division=0),
    )
