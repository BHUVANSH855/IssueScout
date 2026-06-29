from issuescout.models import (
    IssueSummary,
    ScanResult,
)

from issuescout.scanner.fetcher import Fetcher
from issuescout.scanner.pipeline import AnalysisPipeline

from issuescout.scanner.analyzers import (
    AssignmentAnalyzer,
    LinkedPRAnalyzer,
)

from issuescout.scanner.detectors import (
    GitHubLinkedPRDetector,
)
from issuescout.scanner.confidence import ConfidenceCalculator

class ScannerEngine:
    def __init__(
        self,
        fetcher: Fetcher | None = None,
        detector: GitHubLinkedPRDetector | None = None,
        pipeline: AnalysisPipeline | None = None,
        confidence: ConfidenceCalculator | None = None,
    ):
        self.fetcher = fetcher or Fetcher()

        self.detector = detector or GitHubLinkedPRDetector()

        self.pipeline = pipeline or AnalysisPipeline(
            [
                AssignmentAnalyzer(),
                LinkedPRAnalyzer(),
            ]
        )

        self.confidence = confidence or ConfidenceCalculator()

    async def scan_repository(
        self,
        owner: str,
        repo: str,
    ) -> ScanResult:

        try:
            context = await self.fetcher.fetch_context(
                owner,
                repo,
            )
        finally:
            await self.fetcher.close()

        issues = context.issues

        try:
            for issue in issues:
                context.linked_pr_cache[issue.number] = (
                    await self.detector.find_linked_pr(
                        context,
                        issue.number,
                    )
                )
        finally:
            await self.detector.close()

        summaries = []

        for issue in issues:

            results = await self.pipeline.run(
                context,
                issue,
            )

            if not all(result.passed for result in results):
                continue

            linked_pr = context.linked_pr_cache.get(
                issue.number,
            )
            
            summaries.append(
                IssueSummary(
                    number=issue.number,
                    title=issue.title,
                    assigned=issue.assigned,
                    assignee=issue.assignee,
                    confidence=self.confidence.calculate(
                        results,
                    ),
                    linked_pr_number=(
                        linked_pr.number
                        if linked_pr is not None
                        else None
                    ),
                    linked_pr_title=(
                        linked_pr.title
                        if linked_pr is not None
                        else None
                    ),
                )
            )

        return ScanResult(
            repository=f"{owner}/{repo}",
            total_issues=len(summaries),
            available_issues=len(summaries),
            issues=summaries,
        )