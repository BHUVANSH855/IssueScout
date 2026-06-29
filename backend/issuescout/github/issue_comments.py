from issuescout.github.client import GitHubClient


class IssueCommentsAPI:
    def __init__(self):
        self.client = GitHubClient()

    async def get_comments(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ):
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}/comments"

        return await self.client.get(endpoint)

    async def close(self):
        await self.client.close()
