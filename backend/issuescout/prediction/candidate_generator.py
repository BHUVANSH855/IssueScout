from __future__ import annotations

from datetime import timedelta

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

    The goal is to reduce the number of PRs that must be analyzed by the
    relation engine while keeping likely matches.

    The creation date acts as a filtering gate rather than a positive
    matching signal. PRs created far away from the issue creation date
    are ignored before any heuristic matching is performed.
    """

    TITLE_SIMILARITY_THRESHOLD = 45

    CANDIDATE_WINDOW = timedelta(days=90)

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

    def _within_candidate_window(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> bool:
        """
        Reject PRs created too far away from the issue.

        If timestamps are unavailable, do not reject the candidate.
        """

        if issue.created_at is None or pull_request.created_at is None:
            return True

        if pull_request.created_at < issue.created_at:
            return False

        return (pull_request.created_at - issue.created_at) <= self.CANDIDATE_WINDOW

    def _is_candidate(
        self,
        issue: Issue,
        pull_request: PullRequest,
    ) -> bool:

        # First filter by creation time.
        if not self._within_candidate_window(
            issue,
            pull_request,
        ):
            return False

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

        # Shared labels
        if issue.labels & pull_request.labels:
            return True

        return False
