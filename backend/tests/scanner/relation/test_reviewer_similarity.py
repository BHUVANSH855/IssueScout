import pytest

from issuescout.scanner.relation.reviewer_similarity import (
    ReviewerSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_author_is_reviewer():

    analyzer = ReviewerSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
    )

    pr = make_pull_request(
        reviewers={
            "alice",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_author_and_assignee_are_reviewers():

    analyzer = ReviewerSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
        assignee="bob",
    )

    pr = make_pull_request(
        reviewers={
            "alice",
            "bob",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_partial_reviewer_match():

    analyzer = ReviewerSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
        assignee="bob",
    )

    pr = make_pull_request(
        reviewers={
            "alice",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert 0 < result.confidence < 100


@pytest.mark.anyio
async def test_no_reviewer_match():

    analyzer = ReviewerSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
        assignee="bob",
    )

    pr = make_pull_request(
        reviewers={
            "charlie",
            "david",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
