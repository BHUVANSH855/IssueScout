from issuescout.profiles.cpython import CPythonProfile
from issuescout.profiles.generic import GenericProfile
from issuescout.profiles.registry import ProfileRegistry


def test_registry_returns_registered_profile():

    registry = ProfileRegistry()

    profile = registry.get(
        "python/cpython",
    )

    assert isinstance(
        profile,
        CPythonProfile,
    )

    assert profile.full_name == "python/cpython"


def test_registry_returns_generic_profile():

    registry = ProfileRegistry()

    profile = registry.get(
        "numpy/numpy",
    )

    assert isinstance(
        profile,
        GenericProfile,
    )

    assert profile.owner == "numpy"

    assert profile.repository == "numpy"

    assert profile.full_name == "numpy/numpy"
