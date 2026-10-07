"""Manual connectivity check; not an automated test and no URI is printed."""

import os

from dotenv import load_dotenv


def main():
    """Ping the configured MongoDB server with a bounded connection timeout."""
    from pymongo import MongoClient

    load_dotenv()
    uri = os.getenv("MONGO_DB_URL")
    if not uri:
        raise ValueError("Set MONGO_DB_URL first.")
    with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
        client.admin.command("ping")
    print("MongoDB connection successful.")


if __name__ == "__main__":
    main()
