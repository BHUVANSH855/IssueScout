from abc import ABC, abstractmethod

from issuescout.models import (
    AnalysisResult,
    Issue,
    RepositoryScanContext,
)


class BaseAnalyzer(ABC):
    @abstractmethod
    async def analyze(
        self,
        context: RepositoryScanContext,
        issue: Issue,
    ) -> AnalysisResult: ...
