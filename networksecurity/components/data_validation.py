"""Vérifier le schéma et comparer les distributions des deux partitions."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH, TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    """Arrêter le pipeline si le schéma est invalide et conserver le rapport de distribution."""

    def __init__(self, data_ingestion_artifact, data_validation_config):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(file_path):
        """Lire un CSV produit par l’ingestion."""
        return pd.read_csv(file_path)

    def validate_number_of_columns(self, dataframe):
        """Vérifier le nombre et les noms des colonnes attendues."""
        expected = [name for item in self._schema_config["columns"] for name in item]
        return len(dataframe.columns) == len(expected) and set(dataframe.columns) == set(expected)

    def validate_frame(self, dataframe):
        """Contrôler les valeurs numériques, les infinis et les labels de la cible."""
        if not self.validate_number_of_columns(dataframe):
            raise ValueError("Les colonnes ne correspondent pas au schéma data_schema/schema.yaml.")
        values = dataframe.apply(pd.to_numeric, errors="raise")
        if np.isinf(values.to_numpy()).any():
            raise ValueError("Les caractéristiques ne doivent pas contenir de valeur infinie.")
        if values[TARGET_COLUMN].isna().any() or not set(values[TARGET_COLUMN]).issubset({-1, 1}):
            raise ValueError("Result doit contenir uniquement -1 et 1, sans valeur manquante.")
        if values.drop(columns=TARGET_COLUMN).isna().all().any():
            raise ValueError("Une caractéristique ne contient aucune valeur.")
        return values

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        """Écrire le rapport KS ; les p-values ne sont pas corrigées pour les tests multiples."""
        report = {}
        for column in base_df.columns:
            if column == TARGET_COLUMN:
                continue
            p_value = float(ks_2samp(base_df[column].dropna(), current_df[column].dropna()).pvalue)
            report[column] = {"p_value": p_value, "drift_status": p_value < threshold}
        write_yaml_file(self.data_validation_config.drift_report_file_path, report)
        return not any(item["drift_status"] for item in report.values())

    def initiate_data_validation(self):
        """Enregistrer les copies validées et transmettre leurs chemins."""
        train = self.validate_frame(self.read_data(self.data_ingestion_artifact.trained_file_path))
        test = self.validate_frame(self.read_data(self.data_ingestion_artifact.test_file_path))
        self.detect_dataset_drift(train, test)
        config = self.data_validation_config
        for frame, path in [
            (train, config.valid_train_file_path),
            (test, config.valid_test_file_path),
        ]:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            frame.to_csv(path, index=False)
        return DataValidationArtifact(
            True,
            config.valid_train_file_path,
            config.valid_test_file_path,
            None,
            None,
            config.drift_report_file_path,
        )
