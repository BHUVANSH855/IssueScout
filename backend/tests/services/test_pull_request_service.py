from unittest.mock import AsyncMock, patch
from urllib.parse import quote

import pytest

from issuescout.services.pull_request_service import (
    PullRequestService,
)


@pytest.mark.anyio
async def test_search_issue_references():

    with patch(
        "issuescout.services.pull_request_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get = AsyncMock(
            return_value={
                "items": [],
            },
        )

        service = PullRequestService()

        result = await service.search_issue_references(
            "python",
            "cpython",
            123,
        )

        query = 'repo:python/cpython is:pr "123"'

        endpoint = f"/search/issues?q={quote(query)}"

        assert result == {
            "items": [],
        }

        client.get.assert_awaited_once_with(
            endpoint,
        )


@pytest.mark.anyio
async def test_list_open_pull_requests():

    with patch(
        "issuescout.services.pull_request_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get_all = AsyncMock(
            return_value=[],
        )

        service = PullRequestService()

        result = await service.list_open_pull_requests(
            "python",
            "cpython",
        )

        assert result == []

        client.get_all.assert_awaited_once_with(
            "/repos/python/cpython/pulls?state=open",
        )


@pytest.mark.anyio
async def test_get_pull_request_files():

    with patch(
        "issuescout.services.pull_request_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get_all = AsyncMock(
            return_value=[],
        )

        service = PullRequestService()

        await service.get_pull_request_files(
            "python",
            "cpython",
            25,
        )

        client.get_all.assert_awaited_once_with(
            "/repos/python/cpython/pulls/25/files",
        )


@pytest.mark.anyio
async def test_get_pull_request_commits():

    with patch(
        "issuescout.services.pull_request_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.get_all = AsyncMock(
            return_value=[],
        )

        service = PullRequestService()

        await service.get_pull_request_commits(
            "python",
            "cpython",
            25,
        )

        client.get_all.assert_awaited_once_with(
            "/repos/python/cpython/pulls/25/commits",
        )


@pytest.mark.anyio
async def test_close():

    with patch(
        "issuescout.services.pull_request_service.GitHubClient",
    ) as MockClient:
        client = MockClient.return_value

        client.close = AsyncMock()

        service = PullRequestService()

        await service.close()

        client.close.assert_awaited_once()
