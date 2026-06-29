from issuescout.github.client import GitHubClient


class CommitAPI:
    def __init__(self):
        self.client = GitHubClient()

    async def get_commit_pull_requests(
        self,
        owner: str,
        repo: str,
        sha: str,
    ):
        endpoint = f"/repos/{owner}/{repo}/commits/{sha}/pulls"

        return await self.client.get(
            endpoint,
            headers={
                "Accept": ("application/vnd.github+json"),
            },
        )

    async def close(self):
        await self.client.close()
