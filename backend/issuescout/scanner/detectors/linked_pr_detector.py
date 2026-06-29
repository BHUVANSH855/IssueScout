from abc import ABC, abstractmethod

from issuescout.models import (
    PullRequest,
    RepositoryScanContext,
)


class LinkedPRDetector(ABC):
    @abstractmethod
    async def find_linked_pr(
        self,
        context: RepositoryScanContext,
        issue_number: int,
    ) -> PullRequest | None:
        """
        Returns the linked PullRequest if one exists,
        otherwise None.
        """
        raise NotImplementedError
