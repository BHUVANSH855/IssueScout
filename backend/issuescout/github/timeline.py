from issuescout.github.client import GitHubClient


class TimelineAPI:
    def __init__(self):
        self.client = GitHubClient()

    async def get_issue_timeline(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ):
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/timeline"

        return await self.client.get(
            endpoint,
            headers={
                "Accept": ("application/vnd.github+json"),
            },
        )

    async def close(self):
        await self.client.close()
