from issuescout.utils.issue_reference_parser import (
    extract_issue_references,
)


def test_closes_keyword():

    refs = extract_issue_references("Closes #123")

    assert refs == {123}


def test_multiple_keywords():

    refs = extract_issue_references(
        """
        Fixes #10
        Resolves #25
        Closed #40
        """
    )

    assert refs == {
        10,
        25,
        40,
    }


def test_duplicate_references():

    refs = extract_issue_references(
        """
        Fixes #10
        Closes #10
        """
    )

    assert refs == {10}


def test_no_reference():

    refs = extract_issue_references("Improve documentation")

    assert refs == set()


def test_multiple_same_line():

    refs = extract_issue_references("Fixes #1, closes #2, resolves #3")

    assert refs == {
        1,
        2,
        3,
    }


def test_github_issue_url():

    refs = extract_issue_references("https://github.com/python/cpython/issues/12345")

    assert 12345 in refs


def test_cross_repository_reference():

    refs = extract_issue_references("Fixes python/cpython#9876")

    assert 9876 in refs
