from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.prediction.reason_builder import (
    ReasonBuilder,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class TimelineReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="timeline_reference",
        weight=40,
        description="Detects pull requests referenced from the GitHub issue timeline.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matched = (
            hasattr(
                issue,
                "timeline_pull_requests",
            )
            and pull_request.number in issue.timeline_pull_requests
        )

        percentage = 100 if matched else 0

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="timeline_reference",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.timeline_reference(
                    issue.number,
                )
                if matched
                else ReasonBuilder.no_match()
            ),
            evidence_type="strong",
            matched_issue_text=f"Issue #{issue.number}",
            matched_pr_text=f"PR #{pull_request.number}",
            details={
                "matched": matched,
                "issue_number": issue.number,
                "pull_request_number": pull_request.number,
                "timeline_pull_requests": list(
                    getattr(
                        issue,
                        "timeline_pull_requests",
                        [],
                    )
                ),
            },
        )
