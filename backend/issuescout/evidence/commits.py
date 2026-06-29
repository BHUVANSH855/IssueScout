from issuescout.models import (
    Issue,
    Repository,
)


class CommitEvidenceCollector:
    async def collect(
        self,
        repository: Repository,
        issue: Issue,
    ) -> None:
        """
        Populate issue.commit_pull_requests.

        Implementation will be migrated from
        GitHubLinkedPRDetector.
        """

        return
