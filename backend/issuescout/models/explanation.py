from pydantic import BaseModel


class ExplanationItem(BaseModel):
    analyzer: str

    score: int

    confidence: int

    reason: str

    evidence_type: str
