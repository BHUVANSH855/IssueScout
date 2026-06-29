from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.prediction.reason_builder import (
    ReasonBuilder,
)
from issuescout.utils.text_similarity import (
    similarity_percentage,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class AuthorSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="author_similarity",
        weight=10,
        description="Compares issue author with PR author.",
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

        matched = percentage == 100

        return RelationResult(
            analyzer="author_similarity",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.author_match(
                    issue.author,
                )
                if matched
                else ReasonBuilder.author_no_match()
            ),
            evidence_type="supporting",
            matched_issue_text=issue.author,
            matched_pr_text=pull_request.author,
            details={
                "similarity": percentage,
                "issue_author": issue.author,
                "pull_request_author": pull_request.author,
                "matched": matched,
            },
        )
