from issuescout.utils.text_similarity import (
    similarity_percentage,
)


def test_identical_strings():

    assert (
        similarity_percentage(
            "Fix login bug",
            "Fix login bug",
        )
        == 100
    )


def test_completely_different_strings():

    similarity = similarity_percentage(
        "Fix login bug",
        "Add dark mode",
    )

    assert similarity < 40


def test_partial_similarity():

    similarity = similarity_percentage(
        "Fix JSON parser",
        "Fix JSON parser crash",
    )

    assert 50 < similarity < 100


def test_case_insensitive():

    assert (
        similarity_percentage(
            "FIX LOGIN BUG",
            "fix login bug",
        )
        == 100
    )


def test_empty_strings():

    assert (
        similarity_percentage(
            "",
            "",
        )
        == 100
    )


def test_one_empty_string():

    assert (
        similarity_percentage(
            "",
            "hello",
        )
        == 0
    )


def test_whitespace_only():

    assert (
        similarity_percentage(
            "   ",
            "",
        )
        == 100
    )
