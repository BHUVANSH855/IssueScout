from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class LabelSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="label_similarity",
        weight=15,
        description=("Compares issue labels with PR labels."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        common_labels = issue.labels & pull_request.labels

        if issue.labels or pull_request.labels:
            similarity = len(common_labels) / len(issue.labels | pull_request.labels)
        else:
            similarity = 0

        percentage = round(similarity * 100)

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="label_similarity",
            score=score,
            confidence=percentage,
            reason=(f"Label similarity: {percentage}%"),
            matched_issue_text=", ".join(sorted(issue.labels)),
            matched_pr_text=", ".join(sorted(pull_request.labels)),
            details={
                "common_labels": sorted(common_labels),
                "common_count": len(common_labels),
            },
        )
