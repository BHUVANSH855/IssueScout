from issuescout.github.client import GitHubClient


class ReviewService:
    def __init__(self):
        self.client = GitHubClient()

    async def get_reviewers(
        self,
        owner: str,
        repo: str,
        pull_number: int,
    ):
        return await self.client.get(
            f"/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers",
        )

    async def close(self):
        await self.client.close()
