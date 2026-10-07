"""Validate the feature contract and report train/holdout distribution differences."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH, TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    """Reject incompatible data; drift is an informational diagnostic."""

    def __init__(self, data_ingestion_artifact, data_validation_config):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_validation_config = data_validation_config
        self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

    @staticmethod
    def read_data(file_path):
        """Read a persisted ingestion split."""
        return pd.read_csv(file_path)

    def validate_number_of_columns(self, dataframe):
        """Check exact column names rather than only the number of YAML keys."""
        expected = [name for item in self._schema_config["columns"] for name in item]
        return len(dataframe.columns) == len(expected) and set(dataframe.columns) == set(expected)

    def validate_frame(self, dataframe):
        """Enforce numeric finite inputs and the original binary target encoding."""
        if not self.validate_number_of_columns(dataframe):
            raise ValueError("Columns do not match data_schema/schema.yaml.")
        values = dataframe.apply(pd.to_numeric, errors="raise")
        if np.isinf(values.to_numpy()).any():
            raise ValueError("Infinite feature values are not supported.")
        if values[TARGET_COLUMN].isna().any() or not set(values[TARGET_COLUMN]).issubset({-1, 1}):
            raise ValueError("Result must contain only -1 and 1, with no missing target.")
        if values.drop(columns=TARGET_COLUMN).isna().all().any():
            raise ValueError("A feature is entirely missing.")
        return values

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        """Save uncorrected KS p-values; discrete features limit their interpretation."""
        report = {}
        for column in base_df.columns:
            if column == TARGET_COLUMN:
                continue
            p_value = float(ks_2samp(base_df[column].dropna(), current_df[column].dropna()).pvalue)
            report[column] = {"p_value": p_value, "drift_status": p_value < threshold}
        write_yaml_file(self.data_validation_config.drift_report_file_path, report)
        return not any(item["drift_status"] for item in report.values())

    def initiate_data_validation(self):
        """Write validated copies and return their actual paths."""
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
