from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from issuescout.services.commit_service import CommitService

pytestmark = pytest.mark.anyio


def test_constructor():
    with patch("issuescout.services.commit_service.CommitAPI") as mock_api:
        service = CommitService()

        mock_api.assert_called_once()
        assert service.api is mock_api.return_value


async def test_get_commit_pull_requests():
    service = CommitService()
    service.api = MagicMock()
    service.api.get_commit_pull_requests = AsyncMock(return_value=[{"number": 1}])

    result = await service.get_commit_pull_requests(
        "python",
        "cpython",
        "abc123",
    )

    service.api.get_commit_pull_requests.assert_awaited_once_with(
        "python",
        "cpython",
        "abc123",
    )
    assert result == [{"number": 1}]


async def test_close():
    service = CommitService()
    service.api = MagicMock()
    service.api.close = AsyncMock()

    await service.close()

    service.api.close.assert_awaited_once()
