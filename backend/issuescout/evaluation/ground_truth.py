from __future__ import annotations

from datetime import datetime

from issuescout.evaluation.collector.collector import (
    GroundTruthCollector as BaseGroundTruthCollector,
)
from issuescout.evaluation.models import GroundTruthRecord
from issuescout.evaluation.resolvers.timeline import TimelineRelationResolver
from issuescout.services.issue_service import IssueService
from issuescout.services.timeline_service import TimelineService


class GroundTruthCollector(BaseGroundTruthCollector):
    """
    Collects verified Issue → Pull Request relationships from GitHub.

    The collector retrieves issue metadata and timeline events,
    resolves the related pull request, and returns a populated
    GroundTruthRecord.
    """

    def __init__(self) -> None:
        self._issue_service = IssueService()
        self._timeline_service = TimelineService()
        self._resolver = TimelineRelationResolver()

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """
        Convert GitHub ISO-8601 timestamps into datetime objects.
        """

        if not value:
            return None

        return datetime.fromisoformat(
            value.replace(
                "Z",
                "+00:00",
            )
        )

    async def collect(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> GroundTruthRecord:
        """
        Collect one verified ground-truth record.
        """

        issue = await self._issue_service.get_issue(
            owner,
            repository,
            issue_number,
        )

        timeline = await self._timeline_service.get_issue_timeline(
            owner,
            repository,
            issue_number,
        )

        relation = self._resolver.resolve(
            timeline,
        )

        return GroundTruthRecord(
            repository_owner=owner,
            repository_name=repository,
            issue_number=issue_number,
            issue_title=issue.get(
                "title",
                "",
            ),
            issue_state=issue.get(
                "state",
                "unknown",
            ),
            actual_pull_request=relation.pull_request_number,
            issue_created_at=self._parse_datetime(
                issue.get(
                    "created_at",
                )
            ),
            issue_closed_at=self._parse_datetime(
                issue.get(
                    "closed_at",
                )
            ),
            linkage_method=relation.linkage_method,
        )

    async def close(
        self,
    ) -> None:
        """
        Release all underlying resources.
        """

        await self._issue_service.close()
        await self._timeline_service.close()
