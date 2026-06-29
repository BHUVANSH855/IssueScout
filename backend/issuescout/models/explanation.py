from pydantic import BaseModel, Field


class ExplanationItem(BaseModel):
    """
    Represents one piece of evidence contributing to a prediction.
    """

    analyzer: str

    score: int

    confidence: int

    reason: str

    evidence_type: str = "supporting"


class PredictionExplanation(BaseModel):
    """
    Structured explanation for a predicted issue-PR relationship.
    """

    summary: str

    confidence: str

    total_score: int

    items: list[ExplanationItem] = Field(
        default_factory=list,
    )
