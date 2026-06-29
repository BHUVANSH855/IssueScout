from issuescout.github.commits import CommitAPI


class CommitService:
    def __init__(self):
        self.api = CommitAPI()

    async def get_commit_pull_requests(
        self,
        owner: str,
        repo: str,
        sha: str,
    ):
        return await self.api.get_commit_pull_requests(
            owner,
            repo,
            sha,
        )

    async def close(self):
        await self.api.close()
