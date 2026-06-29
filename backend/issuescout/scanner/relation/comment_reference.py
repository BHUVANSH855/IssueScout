from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class CommentReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="comment_reference",
        weight=30,
        description=("Detects PR numbers mentioned inside issue comments."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matched = pull_request.number in issue.comment_pull_requests

        percentage = 100 if matched else 0

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="comment_reference",
            score=score,
            confidence=percentage,
            reason=(
                "PR found in issue comments"
                if matched
                else "No comment reference found"
            ),
            evidence_type="strong",
            matched_issue_text=f"PR #{pull_request.number}",
            matched_pr_text="Issue comments",
            details={
                "matched": matched,
            },
        )
