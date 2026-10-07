"""Optional S3 integration using the separately installed AWS CLI."""

import subprocess


class S3Sync:
    """Execute argument lists without a shell and propagate transfer failures."""

    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """Upload a run directory without deleting remote artifacts."""
        subprocess.run(["aws", "s3", "sync", str(folder), aws_bucket_url], check=True)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        """Download artifacts into a local directory."""
        subprocess.run(["aws", "s3", "sync", aws_bucket_url, str(folder)], check=True)
