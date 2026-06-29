import pytest

from issuescout.scanner.relation.commit_history_similarity import (
    CommitHistorySimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_matching_commit_history():

    analyzer = CommitHistorySimilarityAnalyzer()

    issue = make_issue(
        title="Fix login bug",
    )

    pr = make_pull_request(
        branch_commit_history=[
            "Initial work",
            "Fix login bug",
            "Cleanup",
        ],
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_best_commit_is_used():

    analyzer = CommitHistorySimilarityAnalyzer()

    issue = make_issue(
        title="Improve parser performance",
    )

    pr = make_pull_request(
        branch_commit_history=[
            "Update README",
            "Improve parser performance",
            "Minor cleanup",
        ],
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_unrelated_commit_history():

    analyzer = CommitHistorySimilarityAnalyzer()

    issue = make_issue(
        title="Fix login bug",
    )

    pr = make_pull_request(
        branch_commit_history=[
            "Add dark mode",
            "Update documentation",
            "Refactor tests",
        ],
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score >= 0
    assert result.confidence < 50
