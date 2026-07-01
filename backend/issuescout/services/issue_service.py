from __future__ import annotations

from issuescout.github.issues import IssueAPI


class IssueService:
    """
    High-level service for working with GitHub issues.

    This service provides repository-agnostic issue operations and acts as
    the single entry point for issue-related functionality throughout
    IssueScout.
    """

    def __init__(self) -> None:
        self.issue_api = IssueAPI()

    async def get_issue(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> dict:
        """
        Retrieve a single GitHub issue.
        """
        return await self.issue_api.get_issue(
            owner,
            repository,
            issue_number,
        )

    async def list_open_issues(
        self,
        owner: str,
        repository: str,
    ) -> list[dict]:
        """
        Retrieve all open issues.
        """
        return await self.issue_api.list_open(
            owner,
            repository,
        )

    async def list_closed_issues(
        self,
        owner: str,
        repository: str,
        limit: int = 100,
    ) -> list[dict]:
        """
        Retrieve recently closed issues.
        """
        return await self.issue_api.list_closed(
            owner,
            repository,
            limit=limit,
        )

    async def close(self) -> None:
        """
        Release underlying HTTP resources.
        """
        await self.issue_api.close()
