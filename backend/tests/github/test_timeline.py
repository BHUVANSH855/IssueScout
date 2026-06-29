from unittest.mock import AsyncMock, patch

import pytest

from issuescout.github.timeline import TimelineAPI


def test_timeline_api_creates_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.timeline.GitHubClient",
        return_value=client,
    ):
        api = TimelineAPI()

    assert api.client is client


@pytest.mark.anyio
async def test_get_issue_timeline_calls_expected_endpoint():
    client = AsyncMock()

    client.get.return_value = [
        {
            "event": "cross-referenced",
        }
    ]

    with patch(
        "issuescout.github.timeline.GitHubClient",
        return_value=client,
    ):
        api = TimelineAPI()

    result = await api.get_issue_timeline(
        "python",
        "cpython",
        123,
    )

    client.get.assert_awaited_once_with(
        "/repos/python/cpython/issues/123/timeline",
        headers={
            "Accept": "application/vnd.github+json",
        },
    )

    assert result == [
        {
            "event": "cross-referenced",
        }
    ]


@pytest.mark.anyio
async def test_close_closes_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.timeline.GitHubClient",
        return_value=client,
    ):
        api = TimelineAPI()

    await api.close()

    client.close.assert_awaited_once()
