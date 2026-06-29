from issuescout.models import (
    AnalysisResult,
    Issue,
    RepositoryScanContext,
)

from .base import BaseAnalyzer


class LinkedPRAnalyzer(BaseAnalyzer):
    SCORE = 30

    async def analyze(
        self,
        context: RepositoryScanContext,
        issue: Issue,
    ) -> AnalysisResult:

        linked_pr = context.linked_pr_cache.get(
            issue.number,
        )

        if linked_pr is not None:
            return AnalysisResult(
                analyzer="linked_pr",
                passed=False,
                score=0,
                reason="Linked pull request exists",
            )

        return AnalysisResult(
            analyzer="linked_pr",
            passed=True,
            score=self.SCORE,
            reason="No linked pull request",
        )
