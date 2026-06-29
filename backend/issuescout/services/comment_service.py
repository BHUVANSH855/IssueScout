from issuescout.github.issue_comments import (
    IssueCommentsAPI,
)


class CommentService:
    def __init__(self):
        self.api = IssueCommentsAPI()

    async def get_comments(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ):
        return await self.api.get_comments(
            owner,
            repo,
            issue_number,
        )

    async def close(self):
        await self.api.close()
