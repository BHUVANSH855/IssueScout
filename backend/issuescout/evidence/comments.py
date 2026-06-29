import re

from issuescout.models import (
    Issue,
    PullRequest,
    Repository,
    RepositoryScanContext,
)

from issuescout.services.comment_service import (
    CommentService,
)


class CommentEvidenceCollector:
    def __init__(self):
        self.comment_service = CommentService()

    def _find_cached_pull_request(
        self,
        context: RepositoryScanContext,
        number: int,
    ) -> PullRequest | None:

        for pull_request in context.pull_requests:
            if pull_request.number == number:
                return pull_request

        return None

    async def collect(
        self,
        repository: Repository,
        issue: Issue,
        context: RepositoryScanContext,
    ) -> None:
        """
        Populate issue.comment_pull_requests.
        """

        comments = await self.comment_service.get_comments(
            repository.owner,
            repository.name,
            issue.number,
        )

        issue.comment_pull_requests.clear()

        print(f"Issue #{issue.number}: {len(comments)} comments")

        for comment in comments:
            body = comment.get("body", "")

            matches = {
                int(match)
                for match in re.findall(
                    r"(?:#|GH-)(\d+)",
                    body,
                    flags=re.IGNORECASE,
                )
            }

            matches.update(
                int(match)
                for match in re.findall(
                    r"\bPR\s*#?(\d+)\b",
                    body,
                    flags=re.IGNORECASE,
                )
            )

            matches.update(
                int(match)
                for match in re.findall(
                    r"\bpull\s+request\s+#?(\d+)\b",
                    body,
                    flags=re.IGNORECASE,
                )
            )

            for pr_number in matches:
                cached = self._find_cached_pull_request(
                    context,
                    pr_number,
                )

                if cached is None:
                    continue

                issue.comment_pull_requests.add(
                    cached.number,
                )

                print(f"Comment references PR #{cached.number}")

            if matches:
                print("=" * 100)
                print(f"Issue #{issue.number}")

                print(
                    "Comment PRs:",
                    issue.comment_pull_requests,
                )

    async def close(self):
        await self.comment_service.close()
