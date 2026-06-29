import pytest

from unittest.mock import (
    AsyncMock,
    Mock,
)

from issuescout.core.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)
from issuescout.github.client import GitHubClient


pytestmark = pytest.mark.anyio


async def test_get_raises_authentication_error():
    client = GitHubClient()

    response = Mock()
    response.status_code = 401
    response.text = "Unauthorized"

    client.client.get = AsyncMock(
        return_value=response,
    )

    with pytest.raises(
        GitHubAuthenticationError,
    ):
        await client.get("/repos")


async def test_get_raises_rate_limit_error():
    client = GitHubClient()

    response = Mock()
    response.status_code = 403
    response.text = "Rate limit exceeded"

    client.client.get = AsyncMock(
        return_value=response,
    )

    with pytest.raises(
        GitHubRateLimitError,
    ):
        await client.get("/repos")


async def test_get_raises_not_found_error():
    client = GitHubClient()

    response = Mock()
    response.status_code = 404
    response.text = "Not Found"

    client.client.get = AsyncMock(
        return_value=response,
    )

    with pytest.raises(
        GitHubNotFoundError,
    ):
        await client.get("/missing")


async def test_get_raises_generic_api_error():
    client = GitHubClient()

    response = Mock()
    response.status_code = 500
    response.text = "Internal Server Error"

    client.client.get = AsyncMock(
        return_value=response,
    )

    with pytest.raises(
        GitHubAPIError,
    ):
        await client.get("/repos")
