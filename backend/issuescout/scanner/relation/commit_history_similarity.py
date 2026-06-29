from issuescout.utils.text_similarity import (
    similarity_percentage,
)

from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class CommitHistorySimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="commit_history_similarity",
        weight=20,
        description=(
            "Compares the issue title with "
            "historical commit messages "
            "from the PR branch."
        ),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        highest_similarity = 0
        best_match = ""

        for message in pull_request.branch_commit_history:
            percentage = similarity_percentage(
                issue.title,
                message,
            )

            if percentage > highest_similarity:
                highest_similarity = percentage
                best_match = message

        score = self.scoring.score(
            self.metadata,
            highest_similarity,
        )

        return RelationResult(
            analyzer="commit_history_similarity",
            score=score,
            confidence=highest_similarity,
            reason=(f"Commit history similarity: {highest_similarity}%"),
            matched_issue_text=issue.title,
            matched_pr_text=best_match,
            details={
                "similarity": (f"{highest_similarity}%"),
            },
        )
