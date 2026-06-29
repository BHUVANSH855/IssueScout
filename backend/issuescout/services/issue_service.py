from issuescout.github.client import GitHubClient


class IssueService:
    def __init__(self):
        self.client = GitHubClient()

    async def list_open_issues(
        self,
        owner: str,
        repo: str,
    ):
        return await self.client.get_all(f"/repos/{owner}/{repo}/issues?state=open")

    async def close(self):
        await self.client.close()
