from __future__ import annotations

from abc import ABC, abstractmethod


class RepositoryProfile(ABC):
    """
    Base interface implemented by all repository-specific profiles.

    A profile encapsulates repository-specific conventions used by
    IssueScout without exposing those details to the rest of the system.
    """

    @property
    @abstractmethod
    def owner(
        self,
    ) -> str:
        """
        GitHub repository owner.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def repository(
        self,
    ) -> str:
        """
        GitHub repository name.
        """
        raise NotImplementedError

    @property
    def full_name(
        self,
    ) -> str:
        """
        Fully-qualified repository name.
        """
        return f"{self.owner}/{self.repository}"

    @abstractmethod
    def matches(
        self,
        owner: str,
        repository: str,
    ) -> bool:
        """
        Return True if this profile matches the supplied repository.
        """
        raise NotImplementedError
