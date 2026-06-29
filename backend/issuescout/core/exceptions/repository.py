class RepositoryError(Exception):
    """Base repository exception."""


class RepositoryNotFoundError(RepositoryError):
    """Raised when the requested repository does not exist."""
