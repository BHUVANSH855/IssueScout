from unittest.mock import AsyncMock

import pytest

from issuescout.evidence.comments import (
    CommentEvidenceCollector,
)
from issuescout.models import (
    Repository,
    RepositoryScanContext,
)
from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


def make_context(*pull_requests):
    return RepositoryScanContext(
        repository=Repository(
            owner="python",
            name="cpython",
        ),
        pull_requests=list(pull_requests),
    )


def test_find_cached_pull_request_found():

    collector = CommentEvidenceCollector()

    pr = make_pull_request(number=123)

    context = make_context(pr)

    assert (
        collector._find_cached_pull_request(
            context,
            123,
        )
        is pr
    )


def test_find_cached_pull_request_not_found():

    collector = CommentEvidenceCollector()

    context = make_context()

    assert (
        collector._find_cached_pull_request(
            context,
            999,
        )
        is None
    )


@pytest.mark.anyio
async def test_collect_detects_hash_reference():

    collector = CommentEvidenceCollector()

    collector.comment_service.get_comments = AsyncMock(
        return_value=[
            {
                "body": "Fixed in #10",
            }
        ]
    )

    issue = make_issue()

    pr = make_pull_request(number=10)

    context = make_context(pr)

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.comment_pull_requests == {10}


@pytest.mark.anyio
async def test_collect_detects_pr_reference():

    collector = CommentEvidenceCollector()

    collector.comment_service.get_comments = AsyncMock(
        return_value=[
            {
                "body": "See PR #10",
            }
        ]
    )

    issue = make_issue()

    pr = make_pull_request(number=10)

    context = make_context(pr)

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.comment_pull_requests == {10}


@pytest.mark.anyio
async def test_collect_ignores_unknown_pull_request():

    collector = CommentEvidenceCollector()

    collector.comment_service.get_comments = AsyncMock(
        return_value=[
            {
                "body": "See #999",
            }
        ]
    )

    issue = make_issue()

    context = make_context()

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.comment_pull_requests == set()


@pytest.mark.anyio
async def test_close_closes_service():

    collector = CommentEvidenceCollector()

    collector.comment_service.close = AsyncMock()

    await collector.close()

    collector.comment_service.close.assert_awaited_once()
