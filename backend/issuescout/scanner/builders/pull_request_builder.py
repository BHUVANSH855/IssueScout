from __future__ import annotations

from issuescout.models import PullRequest


class PullRequestBuilder:
    """
    Builds a PullRequest domain model from
    GitHub API responses.
    """

    def build(
        self,
        pull_request: dict,
        *,
        reviewers: dict,
        commits: list[dict],
        branch_commit_history: list[str],
        changed_files: set[str],
    ) -> PullRequest:

        return PullRequest(
            number=pull_request["number"],
            title=pull_request["title"],
            body=pull_request.get("body") or "",
            author=pull_request["user"]["login"],
            branch_name=pull_request["head"]["ref"],
            state=pull_request["state"],
            draft=pull_request["draft"],
            created_at=pull_request.get("created_at"),
            updated_at=pull_request.get("updated_at"),
            closed_at=pull_request.get("closed_at"),
            merged_at=pull_request.get("merged_at"),
            labels={label["name"] for label in pull_request["labels"]},
            reviewers={
                reviewer["login"]
                for reviewer in reviewers.get(
                    "users",
                    [],
                )
            },
            changed_files=changed_files,
            commit_messages=[commit["commit"]["message"] for commit in commits],
            branch_commit_history=branch_commit_history,
        )
