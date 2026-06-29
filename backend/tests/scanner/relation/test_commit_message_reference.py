import pytest

from issuescout.scanner.relation.commit_message_reference import (
    CommitMessageReferenceAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_commit_message_reference_found():

    analyzer = CommitMessageReferenceAnalyzer()

    issue = make_issue(
        number=123,
    )

    pr = make_pull_request(
        related_issues={123},
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_commit_message_references_multiple_issues():

    analyzer = CommitMessageReferenceAnalyzer()

    issue = make_issue(
        number=456,
    )

    pr = make_pull_request(
        related_issues={
            100,
            456,
            999,
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_commit_message_reference_not_found():

    analyzer = CommitMessageReferenceAnalyzer()

    issue = make_issue(
        number=123,
    )

    pr = make_pull_request(
        related_issues={777},
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
