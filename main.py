"""Training CLI: use --source-csv for a demo independent of cloud services."""

import argparse
import json
from dataclasses import asdict

from dotenv import load_dotenv

from networksecurity.pipeline.training_pipeline import TrainingPipeline


def main():
    """Parse the data source and optional artifact upload, then execute one run."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="Train the phishing classification pipeline.")
    parser.add_argument("--source-csv", help="Local labeled CSV; otherwise use MongoDB.")
    parser.add_argument("--sync-s3", action="store_true", help="Upload artifacts using AWS CLI.")
    args = parser.parse_args()
    artifact = TrainingPipeline(args.source_csv, args.sync_s3).run_pipeline()
    print(json.dumps(asdict(artifact), indent=2))


if __name__ == "__main__":
    main()
