from datetime import timedelta

from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class MetadataSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="metadata_similarity",
        weight=10,
        description=(
            "Compares issue and PR metadata such as creation time and author."
        ),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        score = 0
        confidence = 0
        reasons = []

        if issue.author and issue.author == pull_request.author:
            score += 5
            confidence += 30
            reasons.append("Same author")

        if (
            issue.created_at
            and pull_request.created_at
            and pull_request.created_at >= issue.created_at
        ):
            delta = pull_request.created_at - issue.created_at

            if delta <= timedelta(days=7):
                score += 5
                confidence += 70
                reasons.append("PR created shortly after issue")
            elif delta <= timedelta(days=30):
                score += 3
                confidence += 50
                reasons.append("PR created after issue")

        confidence = min(confidence, 100)

        return RelationResult(
            analyzer="metadata_similarity",
            score=score,
            confidence=confidence,
            reason=", ".join(reasons) if reasons else "No metadata match",
            matched_issue_text=issue.title,
            matched_pr_text=pull_request.title,
            details={
                "issue_author": issue.author,
                "pr_author": pull_request.author,
            },
        )
