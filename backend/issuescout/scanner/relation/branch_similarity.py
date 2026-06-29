import re

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


class BranchSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="branch_similarity",
        weight=20,
        description="Matches issue numbers embedded in branch names.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        branch = pull_request.branch_name.lower()

        issue_number = str(issue.number)

        patterns = [
            rf"(^|[/_-]){issue_number}($|[/_-])",
            rf"(^|[/_-])gh[-_/]?{issue_number}($|[/_-])",
            rf"(^|[/_-])issue[-_/]?{issue_number}($|[/_-])",
            rf"(^|[/_-])fix[-_/]?{issue_number}($|[/_-])",
            rf"(^|[/_-])bug[-_/]?{issue_number}($|[/_-])",
            rf"(^|[/_-])cpython[-_/]?{issue_number}($|[/_-])",
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
            reason=(
                ReasonBuilder.branch_match(
                    pull_request.branch_name,
                    issue.number,
                )
                if matched
                else ReasonBuilder.branch_no_match(
                    pull_request.branch_name,
                )
            ),
            evidence_type="strong",
            matched_issue_text=issue_number,
            matched_pr_text=pull_request.branch_name,
            details={
                "matched": matched,
                "branch_name": pull_request.branch_name,
                "issue_number": issue.number,
                "patterns_checked": patterns,
            },
        )
