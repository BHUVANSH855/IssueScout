from issuescout.profiles.generic import GenericProfile


def test_generic_profile_properties():

    profile = GenericProfile(
        owner="numpy",
        repository="numpy",
    )

    assert profile.owner == "numpy"
    assert profile.repository == "numpy"
    assert profile.full_name == "numpy/numpy"
    assert profile.default_branch == "main"


def test_generic_profile_matches():

    profile = GenericProfile(
        owner="pallets",
        repository="flask",
    )

    assert profile.matches(
        "pallets",
        "flask",
    )

    assert not profile.matches(
        "python",
        "cpython",
    )
