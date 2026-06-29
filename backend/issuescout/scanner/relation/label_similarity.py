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


class LabelSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="label_similarity",
        weight=15,
        description="Compares issue labels with pull request labels.",
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        common_labels = issue.labels & pull_request.labels

        all_labels = issue.labels | pull_request.labels

        if all_labels:
            similarity = len(common_labels) / len(all_labels)
        else:
            similarity = 0

        percentage = round(
            similarity * 100,
        )

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="label_similarity",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.label_similarity(
                    len(common_labels),
                    len(all_labels),
                )
                if all_labels
                else ReasonBuilder.no_match()
            ),
            evidence_type="supporting",
            matched_issue_text=", ".join(
                sorted(issue.labels),
            ),
            matched_pr_text=", ".join(
                sorted(pull_request.labels),
            ),
            details={
                "similarity": percentage,
                "common_labels": sorted(common_labels),
                "issue_labels": sorted(issue.labels),
                "pull_request_labels": sorted(
                    pull_request.labels,
                ),
                "common_count": len(common_labels),
                "total_labels": len(all_labels),
            },
        )
