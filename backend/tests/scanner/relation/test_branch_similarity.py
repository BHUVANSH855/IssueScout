import pytest

from issuescout.scanner.relation.branch_similarity import (
    BranchSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_branch_contains_issue_number():

    analyzer = BranchSimilarityAnalyzer()

    issue = make_issue(
        number=123,
    )

    pr = make_pull_request(
        branch_name="fix-123-login",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_branch_contains_gh_prefix():

    analyzer = BranchSimilarityAnalyzer()

    issue = make_issue(
        number=456,
    )

    pr = make_pull_request(
        branch_name="gh-456-fix-docs",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_branch_without_reference():

    analyzer = BranchSimilarityAnalyzer()

    issue = make_issue(
        number=789,
    )

    pr = make_pull_request(
        branch_name="feature/new-ui",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
