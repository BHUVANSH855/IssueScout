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


class CommitReferenceAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="commit_reference",
        weight=45,
        description="Detects PRs referenced by commits associated with an issue.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matched = pull_request.number in issue.commit_pull_requests

        percentage = 100 if matched else 0

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="commit_reference",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.commit_reference(
                    issue.number,
                )
                if matched
                else ReasonBuilder.no_match()
            ),
            evidence_type="strong",
            matched_issue_text=f"PR #{pull_request.number}",
            matched_pr_text=", ".join(
                pull_request.commit_messages,
            ),
            details={
                "matched": matched,
                "issue_number": issue.number,
                "pull_request_number": pull_request.number,
                "commit_messages": pull_request.commit_messages,
            },
        )
