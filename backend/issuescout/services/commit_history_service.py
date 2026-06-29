from issuescout.github.client import GitHubClient


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

        commits = await self.client.get(endpoint)

        return [commit["commit"]["message"] for commit in commits]

    async def close(self):
        await self.client.close()
