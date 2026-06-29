import pytest

from issuescout.models import (
    PullRequest,
    Repository,
    RepositoryScanContext,
)

from issuescout.scanner.analyzers.linked_pr import (
    LinkedPRAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
)


def make_context():

    return RepositoryScanContext(
        repository=Repository(
            owner="python",
            name="cpython",
        ),
    )


@pytest.mark.anyio
async def test_issue_without_linked_pr_passes():

    analyzer = LinkedPRAnalyzer()

    issue = make_issue(
        number=123,
    )

    context = make_context()

    result = await analyzer.analyze(
        context,
        issue,
    )

    assert result.analyzer == "linked_pr"
    assert result.passed is True
    assert result.score == 30
    assert result.reason == "No linked pull request"


@pytest.mark.anyio
async def test_issue_with_linked_pr_fails():

    analyzer = LinkedPRAnalyzer()

    issue = make_issue(
        number=123,
    )

    context = make_context()

    context.linked_pr_cache[123] = PullRequest(
        number=1,
        title="Fix login bug",
        body="",
        branch_name="fix-login",
        author="alice",
    )

    result = await analyzer.analyze(
        context,
        issue,
    )

    assert result.analyzer == "linked_pr"
    assert result.passed is False
    assert result.score == 0
    assert result.reason == "Linked pull request exists"


@pytest.mark.anyio
async def test_cache_is_checked_by_issue_number():

    analyzer = LinkedPRAnalyzer()

    issue = make_issue(
        number=50,
    )

    context = make_context()

    context.linked_pr_cache[99] = PullRequest(
        number=99,
        title="Other PR",
        body="",
        branch_name="other",
        author="bob",
    )

    result = await analyzer.analyze(
        context,
        issue,
    )

    assert result.passed is True
    assert result.score == 30
