from unittest.mock import AsyncMock, patch

import pytest

from issuescout.services.review_service import (
    ReviewService,
)


@pytest.mark.anyio
async def test_get_reviewers():

    with patch(
        "issuescout.services.review_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get = AsyncMock(
            return_value={
                "users": [],
            },
        )

        service = ReviewService()

        result = await service.get_reviewers(
            "python",
            "cpython",
            123,
        )

        assert result == {
            "users": [],
        }

        client.get.assert_awaited_once_with(
            "/repos/python/cpython/pulls/123/requested_reviewers",
        )


@pytest.mark.anyio
async def test_close():

    with patch(
        "issuescout.services.review_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.close = AsyncMock()

        service = ReviewService()

        await service.close()

        client.close.assert_awaited_once()
