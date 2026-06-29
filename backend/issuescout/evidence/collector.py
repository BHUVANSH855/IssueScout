from issuescout.models import (
    Issue,
    RepositoryScanContext,
)

from .comments import (
    CommentEvidenceCollector,
)

from .timeline import (
    TimelineEvidenceCollector,
)


class EvidenceCollector:
    def __init__(self):

        self.timeline = TimelineEvidenceCollector()

        self.comments = CommentEvidenceCollector()

    async def collect(
        self,
        context: RepositoryScanContext,
        issue: Issue,
    ) -> None:
        """
        Collect every available source of evidence
        for an issue.
        """

        await self.timeline.collect(
            context.repository,
            issue,
            context,
        )

        await self.comments.collect(
            context.repository,
            issue,
            context,
        )

    async def close(self):
        await self.timeline.close()
        await self.comments.close()
