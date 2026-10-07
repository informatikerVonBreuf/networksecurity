"""Commande d’entraînement depuis un CSV local ou une collection MongoDB."""

import argparse
import json
from dataclasses import asdict

from dotenv import load_dotenv

from networksecurity.pipeline.training_pipeline import TrainingPipeline


def main():
    """Lire les options et lancer un entraînement."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="Entraîner le pipeline de classification.")
    parser.add_argument(
        "--source-csv", help="CSV local avec la cible ; sinon, lire la collection MongoDB."
    )
    parser.add_argument(
        "--sync-s3", action="store_true", help="Archiver les artefacts sur S3 avec AWS CLI."
    )
    parser.add_argument(
        "--track-mlflow",
        action="store_true",
        help="Enregistrer le modèle et les métriques dans le serveur MLflow configuré.",
    )
    args = parser.parse_args()
    artifact = TrainingPipeline(args.source_csv, args.sync_s3, args.track_mlflow).run_pipeline()
    print(json.dumps(asdict(artifact), indent=2))


if __name__ == "__main__":
    main()
