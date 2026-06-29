from issuescout.models import (
    Issue,
    PullRequest,
    Repository,
    RepositoryScanContext,
)

from issuescout.services.commit_service import (
    CommitService,
)

from issuescout.services.timeline_service import (
    TimelineService,
)


class TimelineEvidenceCollector:
    def __init__(self):
        self.timeline_service = TimelineService()
        self.commit_service = CommitService()

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
        Populate

        - issue.timeline_pull_requests
        - issue.commit_pull_requests
        """

        timeline = await self.timeline_service.get_issue_timeline(
            repository.owner,
            repository.name,
            issue.number,
        )

        issue.timeline_pull_requests.clear()
        issue.commit_pull_requests.clear()

        print(f"Issue #{issue.number}: {len(timeline)} timeline events")

        for event in timeline:
            if event.get("event") != "referenced":
                continue

            sha = event.get("commit_id")

            if not sha:
                continue

            print("=" * 100)
            print(f"Issue #{issue.number}")
            print(f"Commit SHA: {sha}")

            pull_requests = await self.commit_service.get_commit_pull_requests(
                repository.owner,
                repository.name,
                sha,
            )

            print(f"Associated PRs: {len(pull_requests)}")

            for pr in pull_requests:
                cached = self._find_cached_pull_request(
                    context,
                    pr["number"],
                )

                if cached is None:
                    continue

                issue.timeline_pull_requests.add(
                    cached.number,
                )

                issue.commit_pull_requests.add(
                    cached.number,
                )

                print(
                    "Timeline PR set:",
                    issue.timeline_pull_requests,
                )

                print(
                    "Commit PR set:",
                    issue.commit_pull_requests,
                )

                print(f"PR #{cached.number}: {cached.title}")

    async def close(self):
        await self.timeline_service.close()
        await self.commit_service.close()
