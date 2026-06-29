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


class CommentReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="comment_reference",
        weight=30,
        description="Detects pull request references inside issue comments.",
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
                ReasonBuilder.comment_reference(
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
                "comment_pull_requests": list(
                    issue.comment_pull_requests,
                ),
            },
        )
