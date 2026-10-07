"""Conserver ensemble le prétraitement ajusté et le classifieur."""

import numpy as np
import pandas as pd


class NetworkModel:
    """Vérifier les colonnes d’entrée avant d’appliquer le modèle."""

    def __init__(self, preprocessor, model, feature_names):
        self.preprocessor = preprocessor
        self.model = model
        self.feature_names = list(feature_names)

    def predict(self, x):
        """Prédire les classes encodées : 0 pour le label source -1 et 1 pour le label 1."""
        if not isinstance(x, pd.DataFrame) or x.empty:
            raise ValueError("Le fichier CSV doit contenir au moins une ligne.")
        if len(x.columns) != len(self.feature_names) or set(x.columns) != set(self.feature_names):
            raise ValueError(
                "Les colonnes doivent correspondre aux 30 caractéristiques attendues, sans Result."
            )
        values = x.loc[:, self.feature_names].apply(pd.to_numeric, errors="raise")
        if np.isinf(values.to_numpy()).any():
            raise ValueError("Les caractéristiques ne doivent pas contenir de valeur infinie.")
        return self.model.predict(self.preprocessor.transform(values)).astype(int)
