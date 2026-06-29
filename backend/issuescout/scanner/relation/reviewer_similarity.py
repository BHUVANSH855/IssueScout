from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class ReviewerSimilarityAnalyzer(
    RelationAnalyzer,
):
    metadata = AnalyzerMetadata(
        name="reviewer_similarity",
        weight=15,
        description=("Compares issue participants with PR reviewers."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matches = []

        if issue.author and issue.author in pull_request.reviewers:
            matches.append(issue.author)

        if (
            issue.assignee
            and issue.assignee in pull_request.reviewers
            and issue.assignee not in matches
        ):
            matches.append(issue.assignee)

        participant_count = 1 + (1 if issue.assignee else 0)

        percentage = round((len(matches) / participant_count) * 100)

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="reviewer_similarity",
            score=score,
            confidence=percentage,
            reason=(f"Reviewer similarity: {percentage}%"),
            matched_issue_text=", ".join(
                filter(
                    None,
                    [
                        issue.author,
                        issue.assignee,
                    ],
                )
            ),
            matched_pr_text=", ".join(sorted(pull_request.reviewers)),
            details={
                "matched_reviewers": matches,
            },
        )
