from __future__ import annotations


class ReasonBuilder:
    """
    Generates human-readable explanations for relation analyzers.

    Keeping explanation text centralized ensures consistent wording
    across the CLI, JSON output, API responses, and future UI.
    """

    @staticmethod
    def title_similarity(similarity: int) -> str:
        return f"Issue and pull request titles are {similarity}% similar."

    @staticmethod
    def branch_match(
        branch_name: str,
        issue_number: int,
    ) -> str:
        return f"Branch '{branch_name}' references issue #{issue_number}."

    @staticmethod
    def branch_no_match(
        branch_name: str,
    ) -> str:
        return f"Branch '{branch_name}' does not reference the issue."

    @staticmethod
    def author_match(
        author: str,
    ) -> str:
        return f"Issue and pull request were created by '{author}'."

    @staticmethod
    def author_no_match() -> str:
        return "Issue and pull request have different authors."

    @staticmethod
    def label_similarity(
        matched: int,
        total: int,
    ) -> str:
        return f"{matched} of {total} labels match."

    @staticmethod
    def reviewer_similarity(
        matched: int,
        total: int,
    ) -> str:
        return f"{matched} of {total} reviewers match."

    @staticmethod
    def file_similarity(
        matched: int,
        total: int,
    ) -> str:
        return f"{matched} of {total} referenced files match."

    @staticmethod
    def metadata_similarity() -> str:
        return "Issue and pull request share related metadata."

    @staticmethod
    def body_reference(
        issue_number: int,
    ) -> str:
        return f"Pull request description references issue #{issue_number}."

    @staticmethod
    def comment_reference(
        issue_number: int,
    ) -> str:
        return f"A comment references issue #{issue_number}."

    @staticmethod
    def commit_reference(
        issue_number: int,
    ) -> str:
        return f"A linked commit references issue #{issue_number}."

    @staticmethod
    def commit_message_reference(
        issue_number: int,
    ) -> str:
        return f"A commit message references issue #{issue_number}."

    @staticmethod
    def timeline_reference(
        issue_number: int,
    ) -> str:
        return f"The GitHub timeline links this issue to a pull request (issue #{issue_number})."

    @staticmethod
    def commit_history_similarity(
        similarity: int,
    ) -> str:
        return f"The best matching historical commit message is {similarity}% similar to the issue title."

    @staticmethod
    def no_match() -> str:
        return "No meaningful relationship was detected."
