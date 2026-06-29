import pytest

from issuescout.scanner.relation.author_similarity import (
    AuthorSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_same_author_matches():

    analyzer = AuthorSimilarityAnalyzer()

    issue = make_issue(
        author="bhuvansh",
    )

    pr = make_pull_request(
        author="bhuvansh",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_author_match_is_case_insensitive():

    analyzer = AuthorSimilarityAnalyzer()

    issue = make_issue(
        author="Bhuvansh",
    )

    pr = make_pull_request(
        author="bhuvansh",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_different_authors_do_not_match():

    analyzer = AuthorSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
    )

    pr = make_pull_request(
        author="bob",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
