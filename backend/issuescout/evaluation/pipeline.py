from __future__ import annotations

from issuescout.evaluation.comparison.result import ComparisonResult
from issuescout.evaluation.metrics.summary import (
    EvaluationSummary,
    EvaluationSummaryMetric,
)


class EvaluationPipeline:
    """
    High-level orchestration for IssueScout evaluation.

    The pipeline delegates metric computation to
    EvaluationSummaryMetric so that all benchmark metrics
    are computed in a single place.

    Workflow

        Predictions
              │
              ▼
      Comparison Results
              │
              ▼
      EvaluationSummaryMetric
              │
              ▼
      EvaluationSummary
    """

    def __init__(self) -> None:
        self._summary_metric = EvaluationSummaryMetric()

    def summarize(
        self,
        comparisons: list[ComparisonResult],
    ) -> EvaluationSummary:
        """
        Compute all evaluation metrics for a collection
        of comparison results.
        """

        return self._summary_metric.compute(
            comparisons,
        )
