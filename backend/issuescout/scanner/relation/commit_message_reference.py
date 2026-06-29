from issuescout.models import (
    Issue,
    PullRequest,
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
        description=("Detects issue references inside PR commit messages."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        if issue.number in pull_request.related_issues:
            return RelationResult(
                analyzer="commit_message_reference",
                score=COMMIT_REFERENCE_SCORE,
                confidence=100,
                reason=("Issue referenced from commit message."),
                evidence_type="strong",
            )

        return RelationResult(
            analyzer="commit_message_reference",
            score=0,
            confidence=0,
            reason=("No commit message reference found."),
        )
