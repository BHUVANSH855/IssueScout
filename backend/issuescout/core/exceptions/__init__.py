from .github import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)
from .repository import (
    RepositoryError,
    RepositoryNotFoundError,
)
from .scanner import (
    ScannerError,
    ScanFailedError,
)
from .handlers import register_exception_handlers

__all__ = [
    "GitHubAPIError",
    "GitHubAuthenticationError",
    "GitHubNotFoundError",
    "GitHubRateLimitError",
    "RepositoryError",
    "RepositoryNotFoundError",
    "ScannerError",
    "ScanFailedError",
    "register_exception_handlers",
]
