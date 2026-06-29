from issuescout.github.client import GitHubClient
from issuescout.core.exceptions import GitHubNotFoundError


class CommitHistoryService:
    def __init__(self):
        self.client = GitHubClient()

    async def list_branch_commits(
        self,
        owner: str,
        repo: str,
        branch: str,
    ) -> list[str]:
        endpoint = f"/repos/{owner}/{repo}/commits?sha={branch}&per_page=100"

        try:
            commits = await self.client.get(endpoint)
        except GitHubNotFoundError:
            # Branch no longer exists (force-push, deleted branch, etc.)
            # This is expected for many open/old pull requests.
            return []

        return [commit["commit"]["message"] for commit in commits]

    async def close(self):
        await self.client.close()
