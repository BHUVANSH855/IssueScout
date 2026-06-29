from typing import Any

from pydantic import BaseModel, Field


class RelationResult(BaseModel):
    analyzer: str

    score: int

    confidence: int

    reason: str

    evidence_type: str = "supporting"

    matched_issue_text: str | None = None

    matched_pr_text: str | None = None

    details: dict[str, Any] = Field(
        default_factory=dict,
    )
