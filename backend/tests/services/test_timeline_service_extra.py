from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from issuescout.services.timeline_service import TimelineService

pytestmark = pytest.mark.anyio


def test_constructor():
    with patch("issuescout.services.timeline_service.TimelineAPI") as mock_api:
        service = TimelineService()

        mock_api.assert_called_once()
        assert service.timeline is mock_api.return_value


async def test_get_issue_timeline():
    service = TimelineService()
    service.timeline = MagicMock()
    service.timeline.get_issue_timeline = AsyncMock(return_value=[{"event": "closed"}])

    result = await service.get_issue_timeline(
        "python",
        "cpython",
        123,
    )

    service.timeline.get_issue_timeline.assert_awaited_once_with(
        "python",
        "cpython",
        123,
    )
    assert result == [{"event": "closed"}]


async def test_close():
    service = TimelineService()
    service.timeline = MagicMock()
    service.timeline.close = AsyncMock()

    await service.close()

    service.timeline.close.assert_awaited_once()
