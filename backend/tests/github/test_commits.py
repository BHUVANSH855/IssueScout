from unittest.mock import AsyncMock, patch

import pytest

from issuescout.github.commits import CommitAPI


def test_commit_api_creates_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.commits.GitHubClient",
        return_value=client,
    ):
        api = CommitAPI()

    assert api.client is client


@pytest.mark.anyio
async def test_get_commit_pull_requests_calls_expected_endpoint():
    client = AsyncMock()
    client.get.return_value = [{"number": 123}]

    with patch(
        "issuescout.github.commits.GitHubClient",
        return_value=client,
    ):
        api = CommitAPI()

    result = await api.get_commit_pull_requests(
        "python",
        "cpython",
        "abc123",
    )

    client.get.assert_awaited_once_with(
        "/repos/python/cpython/commits/abc123/pulls",
        headers={
            "Accept": "application/vnd.github+json",
        },
    )

    assert result == [{"number": 123}]


@pytest.mark.anyio
async def test_close_closes_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.commits.GitHubClient",
        return_value=client,
    ):
        api = CommitAPI()

    await api.close()

    client.close.assert_awaited_once()