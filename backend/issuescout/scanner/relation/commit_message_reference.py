from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.prediction.reason_builder import (
    ReasonBuilder,
)

from .base import RelationAnalyzer
from .config import COMMIT_REFERENCE_SCORE
from .metadata import AnalyzerMetadata
from .result import RelationResult


class CommitMessageReferenceAnalyzer(
    RelationAnalyzer,
):
    metadata = AnalyzerMetadata(
        name="commit_message_reference",
        weight=45,
        description="Detects issue references inside PR commit messages.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matched = issue.number in pull_request.related_issues

        if matched:
            return RelationResult(
                analyzer="commit_message_reference",
                score=COMMIT_REFERENCE_SCORE,
                confidence=100,
                reason=ReasonBuilder.commit_message_reference(
                    issue.number,
                ),
                evidence_type="strong",
                matched_issue_text=f"#{issue.number}",
                matched_pr_text="\n".join(
                    pull_request.commit_messages,
                ),
                details={
                    "matched": True,
                    "issue_number": issue.number,
                    "commit_messages": pull_request.commit_messages,
                },
            )

        return RelationResult(
            analyzer="commit_message_reference",
            score=0,
            confidence=0,
            reason=ReasonBuilder.no_match(),
            matched_issue_text=f"#{issue.number}",
            matched_pr_text="\n".join(
                pull_request.commit_messages,
            ),
            details={
                "matched": False,
                "issue_number": issue.number,
                "commit_messages": pull_request.commit_messages,
            },
        )
