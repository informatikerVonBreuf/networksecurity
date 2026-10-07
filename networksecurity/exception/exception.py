"""Legacy contextual exception retained for integrations using this import path."""


class NetworkSecurityException(Exception):
    """Add traceback context while remaining safe outside an active exception handler."""

    def __init__(self, error_message, error_details=None):
        traceback = error_details.exc_info()[2] if error_details else None
        self.file_name = traceback.tb_frame.f_code.co_filename if traceback else "unknown"
        self.lineno = traceback.tb_lineno if traceback else None
        super().__init__(f"{self.file_name}:{self.lineno}: {error_message}")
