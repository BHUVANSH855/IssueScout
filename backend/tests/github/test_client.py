from unittest.mock import AsyncMock, Mock, patch

import pytest

from issuescout.github.client import GitHubClient
from issuescout.core.exceptions import (
    GitHubNotFoundError,
)


def test_client_uses_default_headers():
    with patch("issuescout.github.client.httpx.AsyncClient") as async_client:
        GitHubClient()

    headers = async_client.call_args.kwargs["headers"]

    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["User-Agent"] == "IssueScout"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"


def test_client_uses_base_url():
    with patch("issuescout.github.client.httpx.AsyncClient") as async_client:
        GitHubClient()

    assert async_client.call_args.kwargs["base_url"].startswith("https://")


def test_client_uses_timeout():
    with patch("issuescout.github.client.httpx.AsyncClient") as async_client:
        GitHubClient()

    assert async_client.call_args.kwargs["timeout"] == 30.0


@pytest.mark.anyio
async def test_get_returns_json():
    client = GitHubClient()

    response = Mock()
    response.status_code = 200
    response.json.return_value = {"ok": True}
    response.raise_for_status = Mock()

    client.client.get = AsyncMock(
        return_value=response,
    )

    result = await client.get("/repos")

    assert result == {"ok": True}

    client.client.get.assert_awaited_once_with(
        "/repos",
        headers=None,
    )


@pytest.mark.anyio
async def test_get_passes_custom_headers():
    client = GitHubClient()

    response = Mock()
    response.status_code = 200
    response.json.return_value = {}
    response.raise_for_status = Mock()

    client.client.get = AsyncMock(
        return_value=response,
    )

    headers = {
        "If-None-Match": "etag",
    }

    await client.get(
        "/repos",
        headers=headers,
    )

    client.client.get.assert_awaited_once_with(
        "/repos",
        headers=headers,
    )


@pytest.mark.anyio
async def test_get_raises_http_error():
    client = GitHubClient()

    response = Mock()
    response.status_code = 404
    response.text = "Not Found"

    client.client.get = AsyncMock(
        return_value=response,
    )

    with pytest.raises(GitHubNotFoundError):
        await client.get("/missing")


@pytest.mark.anyio
async def test_close_closes_async_client():
    client = GitHubClient()

    client.client.aclose = AsyncMock()

    await client.close()

    client.client.aclose.assert_awaited_once()
