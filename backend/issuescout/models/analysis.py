from pydantic import BaseModel, Field

from issuescout.models.explanation import (
    ExplanationItem,
)
from issuescout.models.pull_request import (
    PullRequest,
)
from issuescout.scanner.relation.result import (
    RelationResult,
)


class AnalysisResult(BaseModel):
    """
    Result produced by a scanner analyzer.
    """

    analyzer: str

    passed: bool

    score: int

    reason: str


class RelationPrediction(BaseModel):
    """
    Prediction produced by the relation engine
    for a single pull request.
    """

    pull_request: PullRequest

    score: int

    results: list[RelationResult]

    strong_evidence: bool = False


class PredictionResult(BaseModel):
    """
    Final prediction returned to the caller.
    """

    issue_number: int

    prediction: RelationPrediction | None = None

    candidates: list[RelationPrediction] = Field(
        default_factory=list,
    )

    accepted: bool = False

    threshold: int = 0

    confidence: str = "Very Low"

    evidence: list[RelationResult] = Field(
        default_factory=list,
    )

    explanation: list[ExplanationItem] = Field(
        default_factory=list,
    )
