import pytest

from issuescout.scanner.relation.title_similarity import (
    TitleSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_identical_titles_match():

    analyzer = TitleSimilarityAnalyzer()

    issue = make_issue(
        title="Fix login bug",
    )

    pr = make_pull_request(
        title="Fix login bug",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_different_titles_have_lower_score():

    analyzer = TitleSimilarityAnalyzer()

    issue = make_issue(
        title="Fix login bug",
    )

    pr = make_pull_request(
        title="Add dark mode support",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score >= 0
    assert result.confidence < 50


@pytest.mark.anyio
async def test_partial_similarity_scores_between_exact_and_unrelated():

    analyzer = TitleSimilarityAnalyzer()

    issue = make_issue(
        title="Fix login bug",
    )

    exact = make_pull_request(
        title="Fix login bug",
    )

    partial = make_pull_request(
        title="Fix login page bug",
    )

    unrelated = make_pull_request(
        title="Add dark mode support",
    )

    exact_result = await analyzer.analyze(
        issue,
        exact,
    )

    partial_result = await analyzer.analyze(
        issue,
        partial,
    )

    unrelated_result = await analyzer.analyze(
        issue,
        unrelated,
    )

    assert exact_result.score >= partial_result.score >= unrelated_result.score
