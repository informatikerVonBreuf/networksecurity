"""Transfert des artefacts S3 avec AWS CLI."""

import subprocess


class S3Sync:
    """Lancer AWS CLI sans shell et signaler les échecs de transfert."""

    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """Envoyer les fichiers d’un entraînement vers S3."""
        subprocess.run(["aws", "s3", "sync", str(folder), aws_bucket_url], check=True)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        """Télécharger les artefacts dans un dossier local."""
        subprocess.run(["aws", "s3", "sync", aws_bucket_url, str(folder)], check=True)
