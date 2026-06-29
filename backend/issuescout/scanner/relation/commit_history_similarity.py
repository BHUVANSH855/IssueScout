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


class CommitHistorySimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="commit_history_similarity",
        weight=20,
        description=(
            "Compares the issue title with "
            "historical commit messages "
            "from the pull request branch."
        ),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        highest_similarity = 0
        best_match = ""
        similar_commits = 0

        for message in pull_request.branch_commit_history:
            percentage = similarity_percentage(
                issue.title,
                message,
            )

            if percentage >= 70:
                similar_commits += 1

            if percentage > highest_similarity:
                highest_similarity = percentage
                best_match = message

        score = self.scoring.score(
            self.metadata,
            highest_similarity,
        )

        if similar_commits >= 2:
            score = min(
                score + 5,
                self.metadata.weight,
            )

        return RelationResult(
            analyzer="commit_history_similarity",
            score=score,
            confidence=highest_similarity,
            reason=(
                ReasonBuilder.commit_history_similarity(
                    highest_similarity,
                )
                if highest_similarity > 0
                else ReasonBuilder.no_match()
            ),
            evidence_type="supporting",
            matched_issue_text=issue.title,
            matched_pr_text=best_match,
            details={
                "similarity": highest_similarity,
                "best_matching_commit": best_match,
                "similar_commit_count": similar_commits,
                "branch_commit_count": len(
                    pull_request.branch_commit_history,
                ),
                "branch_commit_history": (pull_request.branch_commit_history),
            },
        )
