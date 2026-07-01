from __future__ import annotations

from dataclasses import dataclass

from issuescout.evaluation.metrics import (
    EvaluationMetrics,
    calculate_metrics,
)
from issuescout.evaluation.models import RepositoryEvaluation


@dataclass(slots=True)
class EvaluationSummary:
    """
    Summary of a repository evaluation.
    """

    repository: str
    metrics: EvaluationMetrics

    @property
    def passed(self) -> bool:
        """
        Basic success criterion for benchmark runs.

        This can be adjusted later as the prediction engine evolves.
        """
        return self.metrics.top1_accuracy >= 70.0


class Evaluator:
    """
    Orchestrates evaluation of repository prediction results.

    Responsibilities
    ----------------
    - Calculate evaluation metrics
    - Produce repository summaries
    - Aggregate metrics across repositories
    """

    def evaluate(
        self,
        evaluation: RepositoryEvaluation,
    ) -> EvaluationSummary:
        metrics = calculate_metrics(
            evaluation,
        )

        return EvaluationSummary(
            repository=evaluation.full_name,
            metrics=metrics,
        )

    def evaluate_many(
        self,
        evaluations: list[RepositoryEvaluation],
    ) -> list[EvaluationSummary]:
        return [self.evaluate(evaluation) for evaluation in evaluations]

    def aggregate(
        self,
        evaluations: list[RepositoryEvaluation],
    ) -> EvaluationMetrics:
        """
        Aggregate metrics across multiple repositories.
        """

        aggregate = EvaluationMetrics()

        for evaluation in evaluations:
            metrics = calculate_metrics(
                evaluation,
            )

            aggregate.total_issues += metrics.total_issues

            aggregate.top1_correct += metrics.top1_correct
            aggregate.top3_correct += metrics.top3_correct
            aggregate.top5_correct += metrics.top5_correct

            aggregate.true_positive += metrics.true_positive
            aggregate.false_positive += metrics.false_positive
            aggregate.false_negative += metrics.false_negative

        return aggregate
