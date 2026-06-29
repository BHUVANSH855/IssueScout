from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PredictionCandidate:
    """
    Represents a single predicted pull request for an issue.
    """

    pull_request_number: int
    score: float
    confidence: str
    rank: int
    matched: bool = False


@dataclass(slots=True)
class EvaluationRecord:
    """
    Represents one evaluation sample.

    Example:
        Repository: python/cpython
        Issue: #152530
        Actual PR: #152534
        Predicted PRs:
            #152534
            #152467
            #152516
    """

    repository: str
    issue_number: int
    actual_pull_request: int | None
    predictions: list[PredictionCandidate] = field(default_factory=list)


@dataclass(slots=True)
class RepositoryEvaluation:
    """
    Stores all evaluation records for a repository.
    """

    repository: str
    records: list[EvaluationRecord] = field(default_factory=list)
