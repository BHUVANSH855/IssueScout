from issuescout.models.issue import Issue
import asyncio
from issuescout.models.pull_request import PullRequest
from issuescout.models.repository import Repository
from issuescout.models.scan_context import RepositoryScanContext

from issuescout.services.issue_service import IssueService
from issuescout.services.pull_request_service import PullRequestService
from issuescout.services.repository_service import RepositoryService
from issuescout.utils.issue_file_parser import (
    extract_file_mentions,
)
from issuescout.services.review_service import (
    ReviewService,
)
from issuescout.services.commit_history_service import (
    CommitHistoryService,
)


class Fetcher:
    def __init__(self):
        self.issue_service = IssueService()
        self.repository_service = RepositoryService()
        self.pull_request_service = PullRequestService()
        self.review_service = ReviewService()
        self.commit_history_service = CommitHistoryService()

    async def fetch_repository(
        self,
        owner: str,
        repo: str,
    ):
        return await self.repository_service.get_repository(
            owner,
            repo,
        )

    async def fetch_open_issues(
        self,
        owner: str,
        repo: str,
    ):
        github_issues = await self.issue_service.list_open_issues(
            owner,
            repo,
        )

        issues = []

        for issue in github_issues:
            issues.append(
                Issue(
                    number=issue["number"],
                    title=issue["title"],
                    author=issue["user"]["login"],
                    assignee=(
                        issue["assignee"]["login"] if issue["assignee"] else None
                    ),
                    assigned=issue["assignee"] is not None,
                    state=issue["state"],
                    created_at=issue.get("created_at"),
                    updated_at=issue.get("updated_at"),
                    closed_at=issue.get("closed_at"),
                    milestone=(
                        issue["milestone"]["title"] if issue.get("milestone") else None
                    ),
                    labels={label["name"] for label in issue["labels"]},
                    mentioned_files=extract_file_mentions(
                        (issue.get("title") or "") + "\n" + (issue.get("body") or "")
                    ),
                )
            )

        return issues

    async def _build_pull_request(
        self,
        owner: str,
        repo: str,
        pull_request: dict,
    ) -> PullRequest:

        files, reviewers, commits, branch_commit_history = await asyncio.gather(
            self.pull_request_service.get_pull_request_files(
                owner,
                repo,
                pull_request["number"],
            ),
            self.review_service.get_reviewers(
                owner,
                repo,
                pull_request["number"],
            ),
            self.pull_request_service.get_pull_request_commits(
                owner,
                repo,
                pull_request["number"],
            ),
            self.commit_history_service.list_branch_commits(
                owner,
                repo,
                pull_request["head"]["ref"],
            ),
        )

        return PullRequest(
            number=pull_request["number"],
            title=pull_request["title"],
            body=pull_request["body"] or "",
            author=pull_request["user"]["login"],
            branch_name=pull_request["head"]["ref"],
            state=pull_request["state"],
            draft=pull_request["draft"],
            created_at=pull_request.get("created_at"),
            updated_at=pull_request.get("updated_at"),
            closed_at=pull_request.get("closed_at"),
            merged_at=pull_request.get("merged_at"),
            labels={label["name"] for label in pull_request["labels"]},
            reviewers={
                reviewer["login"]
                for reviewer in reviewers.get(
                    "users",
                    [],
                )
            },
            commit_messages=[commit["commit"]["message"] for commit in commits],
            branch_commit_history=branch_commit_history,
        )

    async def fetch_open_pull_requests(
        self,
        owner: str,
        repo: str,
    ):
        github_pull_requests = await self.pull_request_service.list_open_pull_requests(
            owner,
            repo,
        )

        return await asyncio.gather(
            *[
                self._build_pull_request(
                    owner,
                    repo,
                    pull_request,
                )
                for pull_request in github_pull_requests
            ]
        )

    async def fetch_context(
        self,
        owner: str,
        repo: str,
    ) -> RepositoryScanContext:

        repository_data, issues, pull_requests = await asyncio.gather(
            self.fetch_repository(
                owner,
                repo,
            ),
            self.fetch_open_issues(
                owner,
                repo,
            ),
            self.fetch_open_pull_requests(
                owner,
                repo,
            ),
        )

        repository = Repository(
            owner=repository_data["owner"]["login"],
            name=repository_data["name"],
        )

        return RepositoryScanContext(
            repository=repository,
            issues=issues,
            pull_requests=pull_requests,
        )

    async def close(self):
        await self.issue_service.close()
        await self.repository_service.close()
        await self.pull_request_service.close()
        await self.review_service.close()
        await self.commit_history_service.close()
