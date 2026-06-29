from unittest.mock import AsyncMock, patch

import pytest

from issuescout.scanner.fetcher import Fetcher


@pytest.mark.anyio
async def test_fetch_open_issues_empty():

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        issues = await fetcher.fetch_open_issues(
            "python",
            "cpython",
        )

        assert issues == []


@pytest.mark.anyio
async def test_fetch_open_issues_maps_basic_fields():

    github_issue = {
        "number": 123,
        "title": "Fix login bug",
        "body": "",
        "user": {
            "login": "alice",
        },
        "assignee": None,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": [],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issues = await fetcher.fetch_open_issues(
            "python",
            "cpython",
        )

        issue = issues[0]

        assert issue.number == 123
        assert issue.title == "Fix login bug"
        assert issue.author == "alice"
        assert issue.state == "open"


@pytest.mark.anyio
async def test_assigned_issue():

    github_issue = {
        "number": 1,
        "title": "Issue",
        "body": "",
        "user": {
            "login": "alice",
        },
        "assignee": {
            "login": "bob",
        },
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": [],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issue = (
            await fetcher.fetch_open_issues(
                "python",
                "cpython",
            )
        )[0]

        assert issue.assigned is True
        assert issue.assignee == "bob"


@pytest.mark.anyio
async def test_unassigned_issue():

    github_issue = {
        "number": 1,
        "title": "Issue",
        "body": "",
        "user": {
            "login": "alice",
        },
        "assignee": None,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": [],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issue = (
            await fetcher.fetch_open_issues(
                "python",
                "cpython",
            )
        )[0]

        assert issue.assigned is False
        assert issue.assignee is None


@pytest.mark.anyio
async def test_labels_are_converted_to_set():

    github_issue = {
        "number": 1,
        "title": "Issue",
        "body": "",
        "user": {
            "login": "alice",
        },
        "assignee": None,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": [
            {
                "name": "bug",
            },
            {
                "name": "windows",
            },
        ],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issue = (
            await fetcher.fetch_open_issues(
                "python",
                "cpython",
            )
        )[0]

        assert issue.labels == {
            "bug",
            "windows",
        }


@pytest.mark.anyio
async def test_milestone_is_mapped():

    github_issue = {
        "number": 1,
        "title": "Issue",
        "body": "",
        "user": {
            "login": "alice",
        },
        "assignee": None,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": {
            "title": "3.15",
        },
        "labels": [],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issue = (
            await fetcher.fetch_open_issues(
                "python",
                "cpython",
            )
        )[0]

        assert issue.milestone == "3.15"


@pytest.mark.anyio
async def test_file_mentions_are_extracted():

    github_issue = {
        "number": 1,
        "title": "Fix README.md",
        "body": "Update Lib/test/test_json.py",
        "user": {
            "login": "alice",
        },
        "assignee": None,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": [],
    }

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=[
                github_issue,
            ],
        )

        fetcher = Fetcher()

        issue = (
            await fetcher.fetch_open_issues(
                "python",
                "cpython",
            )
        )[0]

        assert "README.md" in issue.mentioned_files
        assert "Lib/test/test_json.py" in issue.mentioned_files


@pytest.mark.anyio
async def test_multiple_issues_are_returned():

    github_issues = []

    for number in range(5):
        github_issues.append(
            {
                "number": number,
                "title": f"Issue {number}",
                "body": "",
                "user": {
                    "login": "alice",
                },
                "assignee": None,
                "state": "open",
                "created_at": None,
                "updated_at": None,
                "closed_at": None,
                "milestone": None,
                "labels": [],
            }
        )

    with patch(
        "issuescout.scanner.fetcher.IssueService",
    ) as MockIssueService:
        service = MockIssueService.return_value

        service.list_open_issues = AsyncMock(
            return_value=github_issues,
        )

        fetcher = Fetcher()

        issues = await fetcher.fetch_open_issues(
            "python",
            "cpython",
        )

        assert len(issues) == 5
