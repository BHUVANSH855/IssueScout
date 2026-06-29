from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class BodyReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="body_reference",
        weight=35,
        description=("Detects issue references inside the PR description."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matched = issue.number in pull_request.related_issues

        percentage = 100 if matched else 0

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="body_reference",
            score=score,
            confidence=percentage,
            reason=(
                "Issue referenced in PR body" if matched else "No issue reference found"
            ),
            evidence_type="strong",
            matched_issue_text=f"#{issue.number}",
            matched_pr_text=pull_request.body,
            details={
                "matched": matched,
            },
        )
