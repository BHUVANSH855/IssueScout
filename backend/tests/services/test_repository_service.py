from unittest.mock import AsyncMock, patch

import pytest

from issuescout.services.repository_service import (
    RepositoryService,
)


@pytest.mark.anyio
async def test_get_repository():

    with patch(
        "issuescout.services.repository_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get = AsyncMock(
            return_value={
                "name": "cpython",
            },
        )

        service = RepositoryService()

        result = await service.get_repository(
            "python",
            "cpython",
        )

        assert result == {
            "name": "cpython",
        }

        client.get.assert_awaited_once_with(
            "/repos/python/cpython",
        )


@pytest.mark.anyio
async def test_close():

    with patch(
        "issuescout.services.repository_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.close = AsyncMock()

        service = RepositoryService()

        await service.close()

        client.close.assert_awaited_once()
