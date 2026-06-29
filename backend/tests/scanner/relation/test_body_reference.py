import pytest

from issuescout.scanner.relation.body_reference import (
    BodyReferenceAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_pr_body_references_issue():

    analyzer = BodyReferenceAnalyzer()

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
async def test_pr_body_references_multiple_issues():

    analyzer = BodyReferenceAnalyzer()

    issue = make_issue(
        number=456,
    )

    pr = make_pull_request(
        related_issues={111, 456, 999},
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_pr_body_without_reference():

    analyzer = BodyReferenceAnalyzer()

    issue = make_issue(
        number=123,
    )

    pr = make_pull_request(
        related_issues={555},
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
