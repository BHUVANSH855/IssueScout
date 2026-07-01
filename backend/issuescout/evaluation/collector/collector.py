from __future__ import annotations

from abc import ABC, abstractmethod

from issuescout.evaluation.models import GroundTruthRecord


class GroundTruthCollector(ABC):
    """
    Base interface for all ground-truth collectors.
    """

    @abstractmethod
    async def collect(
        self,
        owner: str,
        repository: str,
        issue_number: int,
    ) -> GroundTruthRecord:
        """
        Collect one verified Issue → Pull Request relationship.
        """
        raise NotImplementedError
