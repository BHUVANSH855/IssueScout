from issuescout.github.client import GitHubClient


class RepositoryService:
    def __init__(self):
        self.client = GitHubClient()

    async def get_repository(self, owner: str, repo: str):
        return await self.client.get(f"/repos/{owner}/{repo}")

    async def close(self):
        await self.client.close()
