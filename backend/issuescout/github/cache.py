from __future__ import annotations


class GitHubCache:
    """Simple in-memory cache for GitHub API responses."""

    def __init__(self) -> None:
        self._cache: dict[str, object] = {}

    def get(self, key: str):
        return self._cache.get(key)

    def set(
        self,
        key: str,
        value,
    ) -> None:
        self._cache[key] = value

    def clear(self) -> None:
        self._cache.clear()

    def __contains__(
        self,
        key: str,
    ) -> bool:
        return key in self._cache
