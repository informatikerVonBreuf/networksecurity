"""Préparer les tableaux numériques avant l’imputation dans les plis de validation."""

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTER_PARAMS,
    TARGET_COLUMN,
)
from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.utils.main_utils.utils import save_numpy_array_data


class DataTransformation:
    """Encoder la cible sans apprendre de prétraitement avant la validation croisée."""

    def __init__(self, data_validation_artifact, data_transformation_config):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path):
        """Lire une partition validée."""
        return pd.read_csv(file_path)

    @staticmethod
    def get_data_transformer_object():
        """Créer un imputer qui sera ajusté séparément dans chaque pli."""
        return Pipeline([("imputer", KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS))])

    def initiate_data_transformation(self):
        """Enregistrer les tableaux avec la cible encodée dans la dernière colonne."""
        config = self.data_transformation_config
        for source, target in [
            (
                self.data_validation_artifact.valid_train_file_path,
                config.transformed_train_file_path,
            ),
            (self.data_validation_artifact.valid_test_file_path, config.transformed_test_file_path),
        ]:
            df = self.read_data(source)
            labels = df[TARGET_COLUMN].replace(-1, 0)
            array = np.c_[df.drop(columns=TARGET_COLUMN).to_numpy(dtype=float), labels]
            save_numpy_array_data(target, array)
        # Le prétraitement ajusté sera enregistré après la sélection du modèle.
        return DataTransformationArtifact(
            config.transformed_object_file_path,
            config.transformed_train_file_path,
            config.transformed_test_file_path,
        )
