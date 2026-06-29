from unittest.mock import AsyncMock

import pytest

from issuescout.evidence.timeline import (
    TimelineEvidenceCollector,
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

    collector = TimelineEvidenceCollector()

    pr = make_pull_request(number=10)

    context = make_context(pr)

    assert (
        collector._find_cached_pull_request(
            context,
            10,
        )
        is pr
    )


def test_find_cached_pull_request_not_found():

    collector = TimelineEvidenceCollector()

    context = make_context()

    assert (
        collector._find_cached_pull_request(
            context,
            999,
        )
        is None
    )


@pytest.mark.anyio
async def test_collect_with_no_timeline_events():

    collector = TimelineEvidenceCollector()

    collector.timeline_service.get_issue_timeline = AsyncMock(
        return_value=[],
    )

    collector.commit_service.get_commit_pull_requests = AsyncMock()

    issue = make_issue()

    context = make_context()

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.timeline_pull_requests == set()
    assert issue.commit_pull_requests == set()

    collector.commit_service.get_commit_pull_requests.assert_not_called()


@pytest.mark.anyio
async def test_collect_adds_matching_pull_request():

    collector = TimelineEvidenceCollector()

    collector.timeline_service.get_issue_timeline = AsyncMock(
        return_value=[
            {
                "event": "referenced",
                "commit_id": "abc123",
            },
        ],
    )

    collector.commit_service.get_commit_pull_requests = AsyncMock(
        return_value=[
            {
                "number": 10,
            },
        ],
    )

    issue = make_issue()

    pr = make_pull_request(number=10)

    context = make_context(pr)

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.timeline_pull_requests == {10}
    assert issue.commit_pull_requests == {10}


@pytest.mark.anyio
async def test_collect_ignores_unknown_pull_request():

    collector = TimelineEvidenceCollector()

    collector.timeline_service.get_issue_timeline = AsyncMock(
        return_value=[
            {
                "event": "referenced",
                "commit_id": "abc123",
            },
        ],
    )

    collector.commit_service.get_commit_pull_requests = AsyncMock(
        return_value=[
            {
                "number": 999,
            },
        ],
    )

    issue = make_issue()

    context = make_context()

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    assert issue.timeline_pull_requests == set()
    assert issue.commit_pull_requests == set()


@pytest.mark.anyio
async def test_collect_skips_events_without_commit_id():

    collector = TimelineEvidenceCollector()

    collector.timeline_service.get_issue_timeline = AsyncMock(
        return_value=[
            {
                "event": "referenced",
            },
        ],
    )

    collector.commit_service.get_commit_pull_requests = AsyncMock()

    issue = make_issue()

    context = make_context()

    await collector.collect(
        context.repository,
        issue,
        context,
    )

    collector.commit_service.get_commit_pull_requests.assert_not_called()


@pytest.mark.anyio
async def test_close_closes_services():

    collector = TimelineEvidenceCollector()

    collector.timeline_service.close = AsyncMock()
    collector.commit_service.close = AsyncMock()

    await collector.close()

    collector.timeline_service.close.assert_awaited_once()
    collector.commit_service.close.assert_awaited_once()
