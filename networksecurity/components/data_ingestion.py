"""Load a local CSV or MongoDB collection and create a reproducible holdout."""

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    """Persist the raw snapshot and stratified train/test split."""

    def __init__(self, data_ingestion_config, source_csv=None):
        self.data_ingestion_config = data_ingestion_config
        self.source_csv = source_csv

    def export_collection_as_dataframe(self):
        """Read a snapshot; MongoDB connections are opened only when requested."""
        if self.source_csv:
            df = pd.read_csv(self.source_csv)
        else:
            from pymongo import MongoClient

            uri = os.getenv("MONGO_DB_URL")
            if not uri:
                raise ValueError("Set MONGO_DB_URL or pass --source-csv.")
            with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
                config = self.data_ingestion_config
                df = pd.DataFrame(list(client[config.database_name][config.collection_name].find()))
            df = df.drop(columns=["_id"], errors="ignore")
        if df.empty:
            raise ValueError("The data source is empty.")
        return df.replace("na", np.nan)

    def export_data_into_feature_store(self, dataframe):
        """Save the raw snapshot used by this training run."""
        path = Path(self.data_ingestion_config.feature_store_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv(path, index=False)
        return dataframe

    def split_data_as_train_test(self, dataframe):
        """Reserve 20 percent for final evaluation; preserve class proportions."""
        train, test = train_test_split(
            dataframe,
            test_size=self.data_ingestion_config.train_test_split_ratio,
            random_state=42,
            stratify=dataframe[TARGET_COLUMN],
        )
        for frame, path in [
            (train, self.data_ingestion_config.training_file_path),
            (test, self.data_ingestion_config.testing_file_path),
        ]:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            frame.to_csv(path, index=False)

    def initiate_data_ingestion(self):
        """Execute ingestion and return paths consumed by validation."""
        df = self.export_collection_as_dataframe()
        self.export_data_into_feature_store(df)
        self.split_data_as_train_test(df)
        return DataIngestionArtifact(
            self.data_ingestion_config.training_file_path,
            self.data_ingestion_config.testing_file_path,
        )
