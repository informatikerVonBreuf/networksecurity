"""Lecture et écriture des artefacts, comparaison des modèles."""

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold


def read_yaml_file(file_path):
    """Lire un fichier YAML avec le chargeur sécurisé."""
    return yaml.safe_load(Path(file_path).read_text(encoding="utf-8"))


def write_yaml_file(file_path, content, replace=False):
    """Écrire un rapport YAML et créer son dossier si nécessaire."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(content, sort_keys=False), encoding="utf-8")


def save_numpy_array_data(file_path, array):
    """Enregistrer un tableau NumPy sans sérialisation pickle."""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as stream:
        np.save(stream, array, allow_pickle=False)


def load_numpy_array_data(file_path):
    """Lire un tableau produit par le pipeline."""
    return np.load(file_path, allow_pickle=False)


def save_object(file_path, obj):
    """Enregistrer un objet interne au pipeline au format pickle."""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as stream:
        pickle.dump(obj, stream)


def load_object(file_path):
    """Charger un artefact local de confiance avec des versions de dépendances compatibles."""
    with open(file_path, "rb") as stream:
        return pickle.load(stream)


def evaluate_models(X_train, y_train, models, param):
    """Comparer les pipelines sur le F1 de validation croisée, sans utiliser le jeu de test."""
    report = {}
    cv = StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42)
    groups = pd.util.hash_pandas_object(pd.DataFrame(X_train), index=False)
    for name, model in models.items():
        search = GridSearchCV(
            model, param[name], scoring=make_scorer(f1_score, zero_division=0), cv=cv, n_jobs=1
        )
        search.fit(X_train, y_train, groups=groups)
        models[name] = search.best_estimator_
        report[name] = float(search.best_score_)
    return report
