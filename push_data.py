"""Explicit optional CSV import into MongoDB; never runs during module import."""

import argparse
import os

import pandas as pd
from dotenv import load_dotenv


def main():
    """Append records to the configured collection; repeating the command adds duplicates."""
    from pymongo import MongoClient

    load_dotenv()
    parser = argparse.ArgumentParser(description="Append a labeled CSV to MongoDB.")
    parser.add_argument("--source-csv", default="Network_Data/phisingData.csv")
    args = parser.parse_args()
    uri = os.getenv("MONGO_DB_URL")
    if not uri:
        raise ValueError("Set MONGO_DB_URL in your local .env.")
    records = pd.read_csv(args.source_csv).to_dict(orient="records")
    with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
        collection = client[os.getenv("MONGO_DATABASE", "networksecurity")][
            os.getenv("MONGO_COLLECTION", "NetworkData")
        ]
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} records.")


if __name__ == "__main__":
    main()
