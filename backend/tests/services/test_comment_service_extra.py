from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from issuescout.services.comment_service import CommentService

pytestmark = pytest.mark.anyio


def test_constructor():
    with patch("issuescout.services.comment_service.IssueCommentsAPI") as mock_api:
        service = CommentService()

        mock_api.assert_called_once()
        assert service.api is mock_api.return_value


async def test_get_comments():
    service = CommentService()
    service.api = MagicMock()
    service.api.get_comments = AsyncMock(return_value=[{"id": 1}])

    result = await service.get_comments(
        "python",
        "cpython",
        123,
    )

    service.api.get_comments.assert_awaited_once_with(
        "python",
        "cpython",
        123,
    )
    assert result == [{"id": 1}]


async def test_close():
    service = CommentService()
    service.api = MagicMock()
    service.api.close = AsyncMock()

    await service.close()

    service.api.close.assert_awaited_once()
