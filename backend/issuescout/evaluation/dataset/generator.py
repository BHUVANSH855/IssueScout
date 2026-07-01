from __future__ import annotations

from issuescout.evaluation.collector.repository import RepositoryCollector
from issuescout.evaluation.ground_truth import GroundTruthCollector
from issuescout.evaluation.models import RepositoryEvaluation
from issuescout.services.issue_service import IssueService


class DatasetGenerator:
    """
    Generates an evaluation dataset directly from a GitHub repository.

    Workflow

        Repository
            │
            ▼
      Closed Issues
            │
            ▼
      Ground Truth Collector
            │
            ▼
      Repository Collector
            │
            ▼
      Repository Evaluation
    """

    def __init__(self) -> None:
        self._issue_service = IssueService()
        self._ground_truth_collector = GroundTruthCollector()

    async def generate(
        self,
        owner: str,
        repository: str,
        *,
        limit: int = 100,
    ) -> RepositoryEvaluation:
        """
        Generate an evaluation dataset for a repository.
        """

        issues = await self._issue_service.list_closed_issues(
            owner,
            repository,
            limit=limit,
        )

        records = []

        for issue in issues:
            if "pull_request" in issue:
                continue

            record = await self._ground_truth_collector.collect(
                owner,
                repository,
                issue["number"],
            )

            records.append(record)

        collector = RepositoryCollector(
            repository_owner=owner,
            repository_name=repository,
        )

        return collector.build_dataset(records)

    async def close(self) -> None:
        """
        Release all underlying resources.
        """

        await self._issue_service.close()
        await self._ground_truth_collector.close()
