from pydantic import BaseModel, Field

from issuescout.models.issue import Issue
from issuescout.models.pull_request import PullRequest
from issuescout.models.repository import Repository


class RepositoryScanContext(BaseModel):
    repository: Repository

    issues: list[Issue] = Field(default_factory=list)

    pull_requests: list[PullRequest] = Field(default_factory=list)

    linked_pr_cache: dict[int, PullRequest | None] = Field(
        default_factory=dict,
    )
