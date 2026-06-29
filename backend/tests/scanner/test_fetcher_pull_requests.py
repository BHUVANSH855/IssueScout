from unittest.mock import AsyncMock, patch

import pytest

from issuescout.scanner.fetcher import Fetcher


@pytest.mark.anyio
async def test_build_pull_request_maps_basic_fields():

    pull = {
        "number": 10,
        "title": "Fix parser",
        "body": "Body",
        "user": {"login": "alice"},
        "head": {"ref": "fix-parser"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [],
    }

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(
            return_value=[],
        )
        pr_service.get_pull_request_commits = AsyncMock(
            return_value=[],
        )

        review_service.get_reviewers = AsyncMock(
            return_value={"users": []},
        )

        history_service.list_branch_commits = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.number == 10
        assert result.title == "Fix parser"
        assert result.author == "alice"
        assert result.branch_name == "fix-parser"
        assert result.state == "open"
        assert result.draft is False


@pytest.mark.anyio
async def test_body_defaults_to_empty_string():

    pull = {
        "number": 1,
        "title": "Title",
        "body": None,
        "user": {"login": "alice"},
        "head": {"ref": "branch"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [],
    }

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(return_value=[])
        pr_service.get_pull_request_commits = AsyncMock(return_value=[])
        review_service.get_reviewers = AsyncMock(
            return_value={"users": []},
        )
        history_service.list_branch_commits = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.body == ""


@pytest.mark.anyio
async def test_reviewers_are_mapped():

    pull = {
        "number": 1,
        "title": "Title",
        "body": "",
        "user": {"login": "alice"},
        "head": {"ref": "branch"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [],
    }

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(return_value=[])
        pr_service.get_pull_request_commits = AsyncMock(return_value=[])

        review_service.get_reviewers = AsyncMock(
            return_value={
                "users": [
                    {"login": "alice"},
                    {"login": "bob"},
                ],
            },
        )

        history_service.list_branch_commits = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.reviewers == {
            "alice",
            "bob",
        }


@pytest.mark.anyio
async def test_commit_messages_are_mapped():

    pull = {
        "number": 1,
        "title": "Title",
        "body": "",
        "user": {"login": "alice"},
        "head": {"ref": "branch"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [],
    }

    commits = [
        {"commit": {"message": "Fix bug"}},
        {"commit": {"message": "Add tests"}},
    ]

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(return_value=[])
        pr_service.get_pull_request_commits = AsyncMock(
            return_value=commits,
        )

        review_service.get_reviewers = AsyncMock(
            return_value={"users": []},
        )

        history_service.list_branch_commits = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.commit_messages == [
            "Fix bug",
            "Add tests",
        ]


@pytest.mark.anyio
async def test_branch_history_is_mapped():

    pull = {
        "number": 1,
        "title": "Title",
        "body": "",
        "user": {"login": "alice"},
        "head": {"ref": "branch"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [],
    }

    history = [
        "Commit 1",
        "Commit 2",
    ]

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(return_value=[])
        pr_service.get_pull_request_commits = AsyncMock(return_value=[])

        review_service.get_reviewers = AsyncMock(
            return_value={"users": []},
        )

        history_service.list_branch_commits = AsyncMock(
            return_value=history,
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.branch_commit_history == history


@pytest.mark.anyio
async def test_labels_are_mapped_to_set():

    pull = {
        "number": 1,
        "title": "Title",
        "body": "",
        "user": {"login": "alice"},
        "head": {"ref": "branch"},
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": [
            {"name": "bug"},
            {"name": "windows"},
        ],
    }

    with (
        patch(
            "issuescout.scanner.fetcher.PullRequestService",
        ) as MockPRService,
        patch(
            "issuescout.scanner.fetcher.ReviewService",
        ) as MockReviewService,
        patch(
            "issuescout.scanner.fetcher.CommitHistoryService",
        ) as MockHistoryService,
    ):
        pr_service = MockPRService.return_value
        review_service = MockReviewService.return_value
        history_service = MockHistoryService.return_value

        pr_service.get_pull_request_files = AsyncMock(return_value=[])
        pr_service.get_pull_request_commits = AsyncMock(return_value=[])

        review_service.get_reviewers = AsyncMock(
            return_value={"users": []},
        )

        history_service.list_branch_commits = AsyncMock(
            return_value=[],
        )

        fetcher = Fetcher()

        result = await fetcher._build_pull_request(
            "python",
            "cpython",
            pull,
        )

        assert result.labels == {
            "bug",
            "windows",
        }
