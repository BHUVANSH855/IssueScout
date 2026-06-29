from unittest.mock import AsyncMock, patch

import pytest

from issuescout.services.commit_history_service import (
    CommitHistoryService,
)


@pytest.mark.anyio
async def test_list_branch_commits():

    with patch(
        "issuescout.services.commit_history_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get = AsyncMock(
            return_value=[
                {
                    "commit": {
                        "message": "Fix bug",
                    },
                },
                {
                    "commit": {
                        "message": "Add tests",
                    },
                },
            ],
        )

        service = CommitHistoryService()

        result = await service.list_branch_commits(
            "python",
            "cpython",
            "main",
        )

        assert result == [
            "Fix bug",
            "Add tests",
        ]

        client.get.assert_awaited_once_with(
            "/repos/python/cpython/commits?sha=main&per_page=100"
        )


@pytest.mark.anyio
async def test_empty_commit_history():

    with patch(
        "issuescout.services.commit_history_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get = AsyncMock(
            return_value=[],
        )

        service = CommitHistoryService()

        result = await service.list_branch_commits(
            "python",
            "cpython",
            "main",
        )

        assert result == []


@pytest.mark.anyio
async def test_close():

    with patch(
        "issuescout.services.commit_history_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.close = AsyncMock()

        service = CommitHistoryService()

        await service.close()

        client.close.assert_awaited_once()
