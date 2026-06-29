import pytest

from issuescout.scanner.relation.comment_reference import (
    CommentReferenceAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_comment_reference_found():

    analyzer = CommentReferenceAnalyzer()

    issue = make_issue(
        comment_pull_requests={25},
    )

    pr = make_pull_request(
        number=25,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_multiple_comment_references():

    analyzer = CommentReferenceAnalyzer()

    issue = make_issue(
        comment_pull_requests={
            3,
            7,
            12,
        },
    )

    pr = make_pull_request(
        number=7,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_comment_reference_not_found():

    analyzer = CommentReferenceAnalyzer()

    issue = make_issue(
        comment_pull_requests={11},
    )

    pr = make_pull_request(
        number=15,
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
