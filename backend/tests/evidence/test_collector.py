from unittest.mock import AsyncMock

import pytest

from issuescout.evidence.collector import (
    EvidenceCollector,
)
from issuescout.models import (
    Repository,
    RepositoryScanContext,
)
from tests.helpers.factories import (
    make_issue,
)


def test_constructor_creates_collectors():

    collector = EvidenceCollector()

    assert collector.timeline is not None
    assert collector.comments is not None


@pytest.mark.anyio
async def test_collect_calls_timeline_then_comments():

    issue = make_issue()

    context = RepositoryScanContext(
        repository=Repository(
            owner="python",
            name="cpython",
        ),
    )

    collector = EvidenceCollector()

    collector.timeline.collect = AsyncMock()
    collector.comments.collect = AsyncMock()

    await collector.collect(
        context,
        issue,
    )

    collector.timeline.collect.assert_awaited_once_with(
        context.repository,
        issue,
        context,
    )

    collector.comments.collect.assert_awaited_once_with(
        context.repository,
        issue,
        context,
    )


@pytest.mark.anyio
async def test_close_closes_both_collectors():

    collector = EvidenceCollector()

    collector.timeline.close = AsyncMock()
    collector.comments.close = AsyncMock()

    await collector.close()

    collector.timeline.close.assert_awaited_once()
    collector.comments.close.assert_awaited_once()


def test_constructor_creates_new_instances():

    first = EvidenceCollector()
    second = EvidenceCollector()

    assert first.timeline is not second.timeline
    assert first.comments is not second.comments


@pytest.mark.anyio
async def test_collect_propagates_timeline_exception():

    issue = make_issue()

    context = RepositoryScanContext(
        repository=Repository(
            owner="python",
            name="cpython",
        ),
    )

    collector = EvidenceCollector()

    collector.timeline.collect = AsyncMock(
        side_effect=RuntimeError("boom"),
    )
    collector.comments.collect = AsyncMock()

    with pytest.raises(RuntimeError):
        await collector.collect(
            context,
            issue,
        )

    collector.comments.collect.assert_not_called()
