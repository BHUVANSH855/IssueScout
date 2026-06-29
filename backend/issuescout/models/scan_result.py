from pydantic import BaseModel


class IssueSummary(BaseModel):
    number: int
    title: str

    assigned: bool
    assignee: str | None

    confidence: int

    linked_pr_number: int | None = None
    linked_pr_title: str | None = None


class ScanResult(BaseModel):
    repository: str
    total_issues: int
    available_issues: int
    issues: list[IssueSummary]
