"""Vérifier manuellement la connexion MongoDB sans afficher l’URI."""

import os

from dotenv import load_dotenv


def main():
    """Envoyer un ping au serveur MongoDB configuré."""
    from pymongo import MongoClient

    load_dotenv()
    uri = os.getenv("MONGO_DB_URL")
    if not uri:
        raise ValueError("Renseignez MONGO_DB_URL avant de vérifier la connexion.")
    with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
        client.admin.command("ping")
    print("Connexion MongoDB établie.")


if __name__ == "__main__":
    main()
