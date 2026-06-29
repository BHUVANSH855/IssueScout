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


class ReviewerSimilarityAnalyzer(
    RelationAnalyzer,
):
    metadata = AnalyzerMetadata(
        name="reviewer_similarity",
        weight=15,
        description="Compares issue participants with pull request reviewers.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        matches: list[str] = []

        if issue.author and issue.author in pull_request.reviewers:
            matches.append(issue.author)

        if (
            issue.assignee
            and issue.assignee in pull_request.reviewers
            and issue.assignee not in matches
        ):
            matches.append(issue.assignee)

        participant_count = 1 + (1 if issue.assignee else 0)

        percentage = round(
            (len(matches) / participant_count) * 100,
        )

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="reviewer_similarity",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.reviewer_similarity(
                    len(matches),
                    participant_count,
                )
                if matches
                else ReasonBuilder.no_match()
            ),
            evidence_type="supporting",
            matched_issue_text=", ".join(
                filter(
                    None,
                    [
                        issue.author,
                        issue.assignee,
                    ],
                )
            ),
            matched_pr_text=", ".join(
                sorted(
                    pull_request.reviewers,
                )
            ),
            details={
                "similarity": percentage,
                "matched_reviewers": matches,
                "issue_author": issue.author,
                "issue_assignee": issue.assignee,
                "pull_request_reviewers": sorted(
                    pull_request.reviewers,
                ),
                "participant_count": participant_count,
            },
        )
