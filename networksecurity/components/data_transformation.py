"""Prepare raw numeric arrays while preserving missing values for fold-local imputation."""

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
    """Encode -1 as 0 and retain raw features to avoid cross-validation leakage."""

    def __init__(self, data_validation_artifact, data_transformation_config):
        self.data_validation_artifact = data_validation_artifact
        self.data_transformation_config = data_transformation_config

    @staticmethod
    def read_data(file_path):
        """Load a validated data split."""
        return pd.read_csv(file_path)

    @staticmethod
    def get_data_transformer_object():
        """Build a fresh imputer; model selection fits one inside each CV fold."""
        return Pipeline([("imputer", KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS))])

    def initiate_data_transformation(self):
        """Save raw arrays; the last column is the encoded target."""
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
        # The fitted preprocessing object is produced by the model trainer, after CV selection.
        return DataTransformationArtifact(
            config.transformed_object_file_path,
            config.transformed_train_file_path,
            config.transformed_test_file_path,
        )
