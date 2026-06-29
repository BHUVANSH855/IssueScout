from pydantic import BaseModel, Field


class IssueEvidence(BaseModel):
    """
    All evidence collected for a single issue.
    """

    timeline_pull_requests: set[int] = Field(
        default_factory=set,
    )

    comment_pull_requests: set[int] = Field(
        default_factory=set,
    )

    commit_pull_requests: set[int] = Field(
        default_factory=set,
    )

    body_pull_requests: set[int] = Field(
        default_factory=set,
    )
