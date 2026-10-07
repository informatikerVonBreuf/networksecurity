"""Métriques de classification binaire pour la classe positive 1."""

from sklearn.metrics import f1_score, precision_score, recall_score

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact


def get_classification_score(y_true, y_pred):
    """Calculer F1, précision et rappel ; renvoyer zéro si une métrique est indéfinie."""
    return ClassificationMetricArtifact(
        f1_score(y_true, y_pred, zero_division=0),
        precision_score(y_true, y_pred, zero_division=0),
        recall_score(y_true, y_pred, zero_division=0),
    )
