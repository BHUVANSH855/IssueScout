class ScannerError(Exception):
    """Base scanner exception."""


class ScanFailedError(ScannerError):
    """Raised when repository scanning fails."""
