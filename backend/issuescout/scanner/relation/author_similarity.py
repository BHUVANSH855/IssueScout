from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult
from issuescout.utils.text_similarity import (
    similarity_percentage,
)


class AuthorSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="author_similarity",
        weight=10,
        description=("Compares issue author with PR author."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        percentage = similarity_percentage(
            issue.author,
            pull_request.author,
        )

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="author_similarity",
            score=score,
            confidence=percentage,
            reason=f"Author similarity: {percentage}%",
            evidence_type="supporting",
            matched_issue_text=issue.author,
            matched_pr_text=pull_request.author,
            details={
                "similarity": f"{percentage}%",
            },
        )
