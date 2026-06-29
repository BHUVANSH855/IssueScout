from unittest.mock import AsyncMock, patch

import pytest

from issuescout.github.issue_comments import (
    IssueCommentsAPI,
)


def test_issue_comments_api_creates_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.issue_comments.GitHubClient",
        return_value=client,
    ):
        api = IssueCommentsAPI()

    assert api.client is client


@pytest.mark.anyio
async def test_get_comments_calls_expected_endpoint():
    client = AsyncMock()

    client.get.return_value = [
        {
            "id": 1,
        }
    ]

    with patch(
        "issuescout.github.issue_comments.GitHubClient",
        return_value=client,
    ):
        api = IssueCommentsAPI()

    result = await api.get_comments(
        "python",
        "cpython",
        123,
    )

    client.get.assert_awaited_once_with(
        "/repos/python/cpython/issues/123/comments",
    )

    assert result == [
        {
            "id": 1,
        }
    ]


@pytest.mark.anyio
async def test_close_closes_client():
    client = AsyncMock()

    with patch(
        "issuescout.github.issue_comments.GitHubClient",
        return_value=client,
    ):
        api = IssueCommentsAPI()

    await api.close()

    client.close.assert_awaited_once()