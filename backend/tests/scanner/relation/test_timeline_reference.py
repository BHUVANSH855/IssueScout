import pytest

from issuescout.scanner.relation.timeline_reference import (
    TimelineReferenceAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_timeline_reference_found():

    analyzer = TimelineReferenceAnalyzer()

    issue = make_issue(
        timeline_pull_requests={50},
    )

    pr = make_pull_request(
        number=50,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_multiple_timeline_references():

    analyzer = TimelineReferenceAnalyzer()

    issue = make_issue(
        timeline_pull_requests={
            1,
            9,
            21,
        },
    )

    pr = make_pull_request(
        number=9,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_timeline_reference_not_found():

    analyzer = TimelineReferenceAnalyzer()

    issue = make_issue(
        timeline_pull_requests={44},
    )

    pr = make_pull_request(
        number=55,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
