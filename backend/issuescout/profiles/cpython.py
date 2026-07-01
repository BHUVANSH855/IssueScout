from __future__ import annotations

from issuescout.profiles.interfaces import RepositoryProfile


class CPythonProfile(RepositoryProfile):
    """
    Repository profile for CPython.
    """

    @property
    def owner(self) -> str:
        return "python"

    @property
    def repository(self) -> str:
        return "cpython"

    @property
    def default_branch(self) -> str:
        return "main"

    def matches(
        self,
        owner: str,
        repository: str,
    ) -> bool:
        return owner == self.owner and repository == self.repository
