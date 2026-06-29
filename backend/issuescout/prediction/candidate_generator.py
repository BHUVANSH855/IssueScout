from __future__ import annotations

from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.utils.text_similarity import (
    similarity_percentage,
)


class CandidateGenerator:
    """
    Generates a shortlist of candidate pull requests for an issue.

    This reduces the number of PRs that must be analyzed by the
    relation engine while keeping likely matches.
    """

    TITLE_SIMILARITY_THRESHOLD = 30

    def generate(
        self,
        issue: Issue,
        pull_requests: list[PullRequest],
    ) -> list[PullRequest]:

        candidates: list[PullRequest] = []

        for pull_request in pull_requests:
            if self._is_candidate(
                issue,
                pull_request,
            ):
                candidates.append(
                    pull_request,
                )

        return candidates

    def _is_candidate(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> bool:

        # Same author
        if issue.author and issue.author == pull_request.author:
            return True

        # Explicit issue reference
        if issue.number in pull_request.related_issues:
            return True

        # Similar titles
        if (
            similarity_percentage(
                issue.title,
                pull_request.title,
            )
            >= self.TITLE_SIMILARITY_THRESHOLD
        ):
            return True

        # Branch name contains issue number
        if str(issue.number) in pull_request.branch_name:
            return True

        # PR created after issue
        if (
            issue.created_at
            and pull_request.created_at
            and pull_request.created_at >= issue.created_at
        ):
            return True

        # Shared labels
        if issue.labels & pull_request.labels:
            return True

        return False
