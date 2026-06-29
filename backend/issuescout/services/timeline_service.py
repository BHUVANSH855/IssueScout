from issuescout.github.timeline import TimelineAPI


class TimelineService:
    def __init__(self):
        self.timeline = TimelineAPI()

    async def get_issue_timeline(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ):
        return await self.timeline.get_issue_timeline(
            owner,
            repo,
            issue_number,
        )

    async def close(self):
        await self.timeline.close()
