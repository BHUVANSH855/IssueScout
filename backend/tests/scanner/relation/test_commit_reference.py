import pytest

from issuescout.scanner.relation.commit_reference import (
    CommitReferenceAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_commit_reference_found():

    analyzer = CommitReferenceAnalyzer()

    issue = make_issue(
        commit_pull_requests={42},
    )

    pr = make_pull_request(
        number=42,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_multiple_commit_references():

    analyzer = CommitReferenceAnalyzer()

    issue = make_issue(
        commit_pull_requests={
            5,
            17,
            99,
        },
    )

    pr = make_pull_request(
        number=17,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_commit_reference_not_found():

    analyzer = CommitReferenceAnalyzer()

    issue = make_issue(
        commit_pull_requests={10},
    )

    pr = make_pull_request(
        number=20,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
