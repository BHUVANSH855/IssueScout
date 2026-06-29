from unittest.mock import AsyncMock, patch

import pytest

from issuescout.models.issue import Issue
from issuescout.models.pull_request import PullRequest
from issuescout.models.repository import Repository
from issuescout.scanner.fetcher import Fetcher


@pytest.mark.anyio
async def test_fetch_context_builds_repository_scan_context():

    repository_data = {
        "owner": {
            "login": "python",
        },
        "name": "cpython",
    }

    issues = [
        Issue(
            number=1,
            title="Issue",
            author="alice",
        ),
    ]

    pull_requests = [
        PullRequest(
            number=10,
            title="PR",
            body="",
            author="bob",
            branch_name="main",
        ),
    ]

    fetcher = Fetcher()

    with (
        patch.object(
            fetcher,
            "fetch_repository",
            AsyncMock(return_value=repository_data),
        ),
        patch.object(
            fetcher,
            "fetch_open_issues",
            AsyncMock(return_value=issues),
        ),
        patch.object(
            fetcher,
            "fetch_open_pull_requests",
            AsyncMock(return_value=pull_requests),
        ),
    ):
        context = await fetcher.fetch_context(
            "python",
            "cpython",
        )

        assert isinstance(
            context.repository,
            Repository,
        )

        assert context.repository.owner == "python"
        assert context.repository.name == "cpython"

        assert context.issues == issues
        assert context.pull_requests == pull_requests


@pytest.mark.anyio
async def test_fetch_context_calls_all_fetch_methods():

    repository_data = {
        "owner": {
            "login": "python",
        },
        "name": "cpython",
    }

    fetcher = Fetcher()

    with (
        patch.object(
            fetcher,
            "fetch_repository",
            AsyncMock(return_value=repository_data),
        ) as fetch_repository,
        patch.object(
            fetcher,
            "fetch_open_issues",
            AsyncMock(return_value=[]),
        ) as fetch_issues,
        patch.object(
            fetcher,
            "fetch_open_pull_requests",
            AsyncMock(return_value=[]),
        ) as fetch_pulls,
    ):
        await fetcher.fetch_context(
            "python",
            "cpython",
        )

        fetch_repository.assert_awaited_once_with(
            "python",
            "cpython",
        )

        fetch_issues.assert_awaited_once_with(
            "python",
            "cpython",
        )

        fetch_pulls.assert_awaited_once_with(
            "python",
            "cpython",
        )


@pytest.mark.anyio
async def test_fetch_context_with_empty_results():

    repository_data = {
        "owner": {
            "login": "python",
        },
        "name": "cpython",
    }

    fetcher = Fetcher()

    with (
        patch.object(
            fetcher,
            "fetch_repository",
            AsyncMock(return_value=repository_data),
        ),
        patch.object(
            fetcher,
            "fetch_open_issues",
            AsyncMock(return_value=[]),
        ),
        patch.object(
            fetcher,
            "fetch_open_pull_requests",
            AsyncMock(return_value=[]),
        ),
    ):
        context = await fetcher.fetch_context(
            "python",
            "cpython",
        )

        assert context.issues == []
        assert context.pull_requests == []
        assert context.linked_pr_cache == {}
