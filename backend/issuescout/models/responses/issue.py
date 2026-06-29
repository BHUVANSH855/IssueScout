from pydantic import BaseModel


class IssueResponse(BaseModel):
    number: int
    title: str
    assignee: str | None = None
