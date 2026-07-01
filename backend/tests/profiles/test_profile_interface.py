import pytest

from issuescout.profiles.interfaces import RepositoryProfile


def test_repository_profile_is_abstract():

    with pytest.raises(TypeError):
        RepositoryProfile()


def test_repository_profile_full_name():

    class DummyProfile(RepositoryProfile):
        @property
        def owner(self) -> str:
            return "python"

        @property
        def repository(self) -> str:
            return "cpython"

        def matches(
            self,
            owner: str,
            repository: str,
        ) -> bool:
            return owner == self.owner and repository == self.repository

    profile = DummyProfile()

    assert profile.full_name == "python/cpython"
    assert profile.matches(
        "python",
        "cpython",
    )

    assert not profile.matches(
        "numpy",
        "numpy",
    )
