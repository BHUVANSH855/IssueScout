from pathlib import PurePosixPath

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


class FileSimilarityAnalyzer(RelationAnalyzer):
    metadata = AnalyzerMetadata(
        name="file_similarity",
        weight=30,
        description="Matches files mentioned in an issue with files changed by a pull request.",
    )

    @staticmethod
    def _normalize(files: set[str]) -> set[str]:
        """
        Normalize file paths for comparison.

        Examples:
            Lib/test/test_json.py -> lib/test/test_json.py
            TEST_JSON.PY -> test_json.py
        """
        normalized = set()

        for file in files:
            path = PurePosixPath(
                file.replace(
                    "\\",
                    "/",
                )
            )

            normalized.add(
                str(path).lower(),
            )

        return normalized

    async def analyze(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> RelationResult:

        issue_files = self._normalize(
            issue.mentioned_files,
        )

        pr_files = self._normalize(
            pull_request.changed_files,
        )

        overlap = issue_files & pr_files

        all_files = issue_files | pr_files

        if all_files:
            similarity = len(overlap) / len(all_files)
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
            analyzer="file_similarity",
            score=score,
            confidence=percentage,
            reason=(
                ReasonBuilder.file_similarity(
                    len(overlap),
                    len(all_files),
                )
                if all_files
                else ReasonBuilder.no_match()
            ),
            evidence_type="strong",
            matched_issue_text=", ".join(
                sorted(issue_files),
            ),
            matched_pr_text=", ".join(
                sorted(pr_files),
            ),
            details={
                "similarity": percentage,
                "matched_files": sorted(overlap),
                "issue_files": sorted(issue_files),
                "pull_request_files": sorted(pr_files),
                "matched_count": len(overlap),
                "total_files": len(all_files),
            },
        )
