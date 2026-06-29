from issuescout.github.client import GitHubClient


class IssueService:
    def __init__(self):
        self.client = GitHubClient()

    async def list_open_issues(self, owner: str, repo: str):
        return await self.client.get(
            f"/repos/{owner}/{repo}/issues?state=open&per_page=100"
        )

    async def close(self):
        await self.client.close()
