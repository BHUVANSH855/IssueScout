import re

from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class BranchSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="branch_similarity",
        weight=20,
        description=("Matches issue numbers embedded in branch names."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        branch = pull_request.branch_name.lower()

        patterns = [
            rf"\b{issue.number}\b",
            rf"\bgh[-_/]?{issue.number}\b",
            rf"\bissue[-_/]?{issue.number}\b",
            rf"\bfix[-_/]?{issue.number}\b",
            rf"\bbug[-_/]?{issue.number}\b",
        ]

        matched = any(
            re.search(
                pattern,
                branch,
                flags=re.IGNORECASE,
            )
            for pattern in patterns
        )

        percentage = 100 if matched else 0

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="branch_similarity",
            score=score,
            confidence=percentage,
            reason=(f"Branch similarity: {percentage}%"),
            evidence_type="strong",
            matched_issue_text=str(issue.number),
            matched_pr_text=pull_request.branch_name,
            details={
                "matched": matched,
            },
        )
