from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class TimelineReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="timeline_reference",
        weight=40,
        description=("Timeline referenced commit linked to PR."),
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
                "PR found from issue timeline"
                if matched
                else "No timeline reference found"
            ),
            evidence_type="strong",
            matched_issue_text=f"PR #{pull_request.number}",
            matched_pr_text="Issue timeline",
            details={
                "matched": matched,
            },
        )
