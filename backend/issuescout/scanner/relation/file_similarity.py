from issuescout.models import (
    Issue,
    PullRequest,
)

from .base import RelationAnalyzer
from .metadata import AnalyzerMetadata
from .result import RelationResult


class FileSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="file_similarity",
        weight=30,
        description=("Matches files mentioned in an issue with files changed by a PR."),
    )

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        overlap = issue.mentioned_files & pull_request.changed_files

        if issue.mentioned_files or pull_request.changed_files:
            similarity = len(overlap) / len(
                issue.mentioned_files | pull_request.changed_files
            )
        else:
            similarity = 0

        percentage = round(similarity * 100)

        score = self.scoring.score(
            self.metadata,
            percentage,
        )

        return RelationResult(
            analyzer="file_similarity",
            score=score,
            confidence=percentage,
            reason=(f"File similarity: {percentage}%"),
            evidence_type="strong",
            matched_issue_text=", ".join(sorted(issue.mentioned_files)),
            matched_pr_text=", ".join(sorted(pull_request.changed_files)),
            details={
                "matched_files": sorted(overlap),
                "matched_count": len(overlap),
            },
        )
