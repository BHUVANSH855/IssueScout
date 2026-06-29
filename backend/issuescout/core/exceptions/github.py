class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""


class GitHubAuthenticationError(GitHubAPIError):
    """Raised when GitHub authentication fails."""


class GitHubRateLimitError(GitHubAPIError):
    """Raised when the GitHub API rate limit is exceeded."""


class GitHubNotFoundError(GitHubAPIError):
    """Raised when a GitHub resource cannot be found."""
