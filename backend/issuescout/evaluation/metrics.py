from __future__ import annotations

from dataclasses import dataclass

from issuescout.evaluation.models import RepositoryEvaluation


@dataclass(slots=True)
class EvaluationMetrics:
    """
    Stores benchmark statistics for an evaluation run.
    """

    total_issues: int = 0
    top1_correct: int = 0
    top3_correct: int = 0
    top5_correct: int = 0

    @property
    def top1_accuracy(self) -> float:
        if self.total_issues == 0:
            return 0.0
        return (self.top1_correct / self.total_issues) * 100

    @property
    def top3_accuracy(self) -> float:
        if self.total_issues == 0:
            return 0.0
        return (self.top3_correct / self.total_issues) * 100

    @property
    def top5_accuracy(self) -> float:
        if self.total_issues == 0:
            return 0.0
        return (self.top5_correct / self.total_issues) * 100


def calculate_metrics(
    evaluation: RepositoryEvaluation,
) -> EvaluationMetrics:
    """
    Calculate Top-1, Top-3 and Top-5 accuracy for a repository evaluation.
    """

    metrics = EvaluationMetrics()

    metrics.total_issues = len(evaluation.records)

    for record in evaluation.records:
        actual = record.actual_pull_request

        if actual is None:
            continue

        predictions = sorted(
            record.predictions,
            key=lambda prediction: prediction.rank,
        )

        if any(
            prediction.pull_request_number == actual for prediction in predictions[:1]
        ):
            metrics.top1_correct += 1

        if any(
            prediction.pull_request_number == actual for prediction in predictions[:3]
        ):
            metrics.top3_correct += 1

        if any(
            prediction.pull_request_number == actual for prediction in predictions[:5]
        ):
            metrics.top5_correct += 1

    return metrics
