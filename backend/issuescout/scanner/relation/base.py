from abc import ABC, abstractmethod

from .metadata import AnalyzerMetadata
from .scoring import ScoringPolicy


class RelationAnalyzer(ABC):
    metadata = AnalyzerMetadata(
        name="base",
        weight=0,
    )

    scoring = ScoringPolicy()

    @abstractmethod
    async def analyze(
        self,
        issue,
        pull_request,
    ): ...
