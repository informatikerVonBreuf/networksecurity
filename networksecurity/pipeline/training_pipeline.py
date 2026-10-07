"""Orchestrate the four training stages with optional explicit S3 publication."""

import os

from networksecurity.cloud.s3_syncer import S3Sync
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
)
from networksecurity.logging.logger import logging


class TrainingPipeline:
    """Run locally by default; remote services require explicit configuration."""

    def __init__(self, source_csv=None, sync_s3=False, track_mlflow=False):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.source_csv = source_csv
        self.sync_s3 = sync_s3
        self.track_mlflow = track_mlflow

    def run_pipeline(self):
        """Execute stages in dependency order and return the model artifact."""
        config = self.training_pipeline_config
        bucket = os.getenv("TRAINING_BUCKET_NAME")
        if self.sync_s3 and not bucket:
            raise ValueError("Set TRAINING_BUCKET_NAME before requesting --sync-s3.")
        logging.info("Starting training run %s", config.timestamp)
        ingestion = DataIngestion(
            DataIngestionConfig(config), self.source_csv
        ).initiate_data_ingestion()
        validation = DataValidation(
            ingestion, DataValidationConfig(config)
        ).initiate_data_validation()
        transformation = DataTransformation(
            validation, DataTransformationConfig(config)
        ).initiate_data_transformation()
        model = ModelTrainer(
            ModelTrainerConfig(config), transformation, track=self.track_mlflow
        ).initiate_model_trainer()
        if self.sync_s3:
            sync = S3Sync()
            sync.sync_folder_to_s3(
                config.artifact_dir, f"s3://{bucket}/artifacts/{config.timestamp}"
            )
            sync.sync_folder_to_s3(
                config.model_dir, f"s3://{bucket}/final_model/{config.timestamp}"
            )
        logging.info("Training completed: %s", model)
        return model
