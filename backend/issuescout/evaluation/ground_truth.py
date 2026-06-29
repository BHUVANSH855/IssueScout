from __future__ import annotations

from dataclasses import dataclass

from issuescout.github.client import GitHubClient


@dataclass(slots=True)
class GroundTruthRecord:
    """
    Represents the actual pull request linked to a GitHub issue.
    """

    repository: str
    issue_number: int
    actual_pull_request: int | None


class GroundTruthCollector:
    """
    Collects ground-truth issue → pull request mappings from GitHub.
    """

    def __init__(self) -> None:
        self.client = GitHubClient()

    async def collect(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> GroundTruthRecord:
        """
        Collect the actual pull request linked to an issue.

        Currently this is a placeholder implementation.
        Timeline-based matching will be implemented next.
        """

        return GroundTruthRecord(
            repository=f"{owner}/{repository}",
            issue_number=issue_number,
            actual_pull_request=None,
        )

    async def close(self) -> None:
        await self.client.close()
