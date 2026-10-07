"""Importer un CSV dans MongoDB depuis la ligne de commande."""

import argparse
import os

import pandas as pd
from dotenv import load_dotenv


def main():
    """Ajouter les lignes à la collection ; un nouvel import ajoute de nouveaux documents."""
    from pymongo import MongoClient

    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Ajouter les lignes d’un CSV à la collection MongoDB."
    )
    parser.add_argument("--source-csv", default="Network_Data/phisingData.csv")
    args = parser.parse_args()
    uri = os.getenv("MONGO_DB_URL")
    if not uri:
        raise ValueError("Renseignez MONGO_DB_URL dans votre fichier .env.")
    records = pd.read_csv(args.source_csv).to_dict(orient="records")
    with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
        collection = client[os.getenv("MONGO_DATABASE", "networksecurity")][
            os.getenv("MONGO_COLLECTION", "NetworkData")
        ]
        result = collection.insert_many(records)
        print(f"{len(result.inserted_ids)} documents ajoutés.")


if __name__ == "__main__":
    main()
