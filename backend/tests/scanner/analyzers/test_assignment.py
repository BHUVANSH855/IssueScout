import pytest

from issuescout.models import (
    Repository,
    RepositoryScanContext,
)

from issuescout.scanner.analyzers.assignment import (
    AssignmentAnalyzer,
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
async def test_unassigned_issue_passes():

    analyzer = AssignmentAnalyzer()

    issue = make_issue(
        assigned=False,
    )

    result = await analyzer.analyze(
        make_context(),
        issue,
    )

    assert result.passed is True
    assert result.score == 20
    assert result.reason == "Issue is unassigned"


@pytest.mark.anyio
async def test_assigned_issue_fails():

    analyzer = AssignmentAnalyzer()

    issue = make_issue(
        assigned=True,
    )

    result = await analyzer.analyze(
        make_context(),
        issue,
    )

    assert result.passed is False
    assert result.score == 0
    assert result.reason == "Issue already assigned"


@pytest.mark.anyio
async def test_analyzer_name():

    analyzer = AssignmentAnalyzer()

    result = await analyzer.analyze(
        make_context(),
        make_issue(),
    )

    assert result.analyzer == "assignment"
