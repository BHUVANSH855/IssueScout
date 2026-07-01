from __future__ import annotations

from issuescout.profiles.interfaces import RepositoryProfile


class GenericProfile(RepositoryProfile):
    """
    Default repository profile.

    Used whenever no repository-specific profile has been registered.
    """

    def __init__(
        self,
        owner: str,
        repository: str,
    ) -> None:
        self._owner = owner
        self._repository = repository

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def repository(self) -> str:
        return self._repository

    @property
    def default_branch(self) -> str:
        """
        Default branch used by most GitHub repositories.
        """
        return "main"

    def matches(
        self,
        owner: str,
        repository: str,
    ) -> bool:
        return owner == self.owner and repository == self.repository
