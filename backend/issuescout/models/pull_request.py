from datetime import datetime

from pydantic import BaseModel, Field


class PullRequest(BaseModel):
    number: int

    title: str

    body: str

    branch_name: str

    author: str

    state: str = "open"

    draft: bool = False

    created_at: datetime | None = None

    updated_at: datetime | None = None

    closed_at: datetime | None = None

    merged_at: datetime | None = None

    labels: set[str] = Field(
        default_factory=set,
    )

    changed_files: set[str] = Field(
        default_factory=set,
    )

    commit_messages: list[str] = Field(
        default_factory=list,
    )

    branch_commit_history: list[str] = Field(
        default_factory=list,
    )

    related_issues: set[int] = Field(
        default_factory=set,
    )

    reviewers: set[str] = Field(
        default_factory=set,
    )
