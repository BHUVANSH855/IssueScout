from __future__ import annotations

from issuescout.profiles.cpython import CPythonProfile
from issuescout.profiles.generic import GenericProfile
from issuescout.profiles.interfaces import RepositoryProfile


class ProfileRegistry:
    """
    Registry of supported repository profiles.

    Known repositories return specialized profiles.
    Unknown repositories fall back to a GenericProfile.
    """

    def __init__(self) -> None:
        self._profiles: dict[str, RepositoryProfile] = {
            "python/cpython": CPythonProfile(),
        }

    def get(
        self,
        full_name: str,
    ) -> RepositoryProfile:
        """
        Retrieve a repository profile.

        Unknown repositories automatically receive a GenericProfile.
        """

        profile = self._profiles.get(full_name)

        if profile is not None:
            return profile

        owner, repository = full_name.split("/", 1)

        return GenericProfile(
            owner=owner,
            repository=repository,
        )

    def all(
        self,
    ) -> list[RepositoryProfile]:
        """
        Return all registered repository profiles.
        """
        return list(self._profiles.values())
