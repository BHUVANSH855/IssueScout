from unittest.mock import AsyncMock, patch

import pytest

from issuescout.services.issue_service import (
    IssueService,
)


@pytest.mark.anyio
async def test_list_open_issues():

    with patch(
        "issuescout.services.issue_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get_all = AsyncMock(
            return_value=[
                {
                    "number": 1,
                },
            ],
        )

        service = IssueService()

        result = await service.list_open_issues(
            "python",
            "cpython",
        )

        assert result == [
            {
                "number": 1,
            },
        ]

        client.get_all.assert_awaited_once_with(
            "/repos/python/cpython/issues?state=open",
        )


@pytest.mark.anyio
async def test_close():

    with patch(
        "issuescout.services.issue_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.close = AsyncMock()

        service = IssueService()

        await service.close()

        client.close.assert_awaited_once()
