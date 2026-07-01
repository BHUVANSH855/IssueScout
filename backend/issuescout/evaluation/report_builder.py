from __future__ import annotations

from issuescout.evaluation.comparison.result import ComparisonResult
from issuescout.evaluation.metrics.summary import EvaluationSummary
from issuescout.evaluation.report import (
    EvaluationFailure,
    EvaluationReport,
    RepositoryMetrics,
)


class ReportBuilder:
    """
    Builds EvaluationReport instances from evaluation summaries and
    comparison results.
    """

    def build(
        self,
        repository: str,
        summary: EvaluationSummary,
        comparisons: list[ComparisonResult],
    ) -> EvaluationReport:
        metrics = RepositoryMetrics(
            total_issues=summary.issue_count,
            evaluated_issues=summary.issue_count,
            top1_accuracy=summary.accuracy,
        )

        failures: list[EvaluationFailure] = []

        for comparison in comparisons:
            if comparison.matched:
                continue

            failures.append(
                EvaluationFailure(
                    issue_number=comparison.issue_number,
                    actual_pull_request=comparison.actual_pull_request,
                    predicted_pull_request=comparison.predicted_pull_request,
                    predicted_rank=comparison.rank,
                    prediction_score=comparison.confidence,
                    reason="Prediction did not match ground truth.",
                )
            )

        return EvaluationReport(
            repository=repository,
            metrics=metrics,
            failures=failures,
        )
