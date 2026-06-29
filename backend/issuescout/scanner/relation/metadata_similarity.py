from datetime import timedelta

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


class MetadataSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="metadata_similarity",
        weight=10,
        description=(
            "Compares issue and pull request metadata such as authors and timestamps."
        ),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        score = 0
        confidence = 0
        reasons: list[str] = []

        same_author = bool(issue.author) and issue.author == pull_request.author

        created_delta_days: int | None = None
        updated_delta_days: int | None = None

        # Same author
        if same_author:
            score += 5
            confidence += 30
            reasons.append(
                ReasonBuilder.author_match(
                    issue.author,
                )
            )

        # PR created after issue
        if (
            issue.created_at
            and pull_request.created_at
            and pull_request.created_at >= issue.created_at
        ):
            delta = pull_request.created_at - issue.created_at
            created_delta_days = delta.days

            if delta <= timedelta(days=7):
                score += 5
                confidence += 70
                reasons.append("Pull request was created within 7 days of the issue.")

            elif delta <= timedelta(days=30):
                score += 3
                confidence += 50
                reasons.append("Pull request was created within 30 days of the issue.")

        # Issue updated shortly before PR creation
        if (
            issue.updated_at
            and pull_request.created_at
            and issue.updated_at <= pull_request.created_at
        ):
            delta = pull_request.created_at - issue.updated_at
            updated_delta_days = delta.days

            if delta <= timedelta(days=3):
                score += 2
                confidence += 20
                reasons.append("Issue was updated shortly before the pull request.")

        score = min(
            score,
            self.metadata.weight,
        )

        confidence = min(
            confidence,
            100,
        )

        return RelationResult(
            analyzer="metadata_similarity",
            score=score,
            confidence=confidence,
            reason=("; ".join(reasons) if reasons else ReasonBuilder.no_match()),
            evidence_type="supporting",
            matched_issue_text=issue.title,
            matched_pr_text=pull_request.title,
            details={
                "same_author": same_author,
                "issue_author": issue.author,
                "pull_request_author": pull_request.author,
                "issue_created_at": issue.created_at,
                "pull_request_created_at": pull_request.created_at,
                "issue_updated_at": issue.updated_at,
                "created_after_days": created_delta_days,
                "updated_after_days": updated_delta_days,
            },
        )
