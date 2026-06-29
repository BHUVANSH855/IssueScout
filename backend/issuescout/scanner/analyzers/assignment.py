from issuescout.models import (
    AnalysisResult,
    Issue,
    RepositoryScanContext,
)

from .base import BaseAnalyzer


class AssignmentAnalyzer(BaseAnalyzer):
    async def analyze(
        self,
        context: RepositoryScanContext,
        issue: Issue,
    ) -> AnalysisResult:

        if issue.assigned:
            return AnalysisResult(
                analyzer="assignment",
                passed=False,
                score=0,
                reason="Issue already assigned",
            )

        return AnalysisResult(
            analyzer="assignment",
            passed=True,
            score=20,
            reason="Issue is unassigned",
        )
