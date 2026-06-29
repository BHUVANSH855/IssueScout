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

    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0

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

    @property
    def precision(self) -> float:
        denominator = self.true_positive + self.false_positive
        if denominator == 0:
            return 0.0
        return (self.true_positive / denominator) * 100

    @property
    def recall(self) -> float:
        denominator = self.true_positive + self.false_negative
        if denominator == 0:
            return 0.0
        return (self.true_positive / denominator) * 100

    @property
    def f1_score(self) -> float:
        precision = self.precision
        recall = self.recall

        if precision + recall == 0:
            return 0.0

        return 2 * precision * recall / (precision + recall)


def calculate_metrics(
    evaluation: RepositoryEvaluation,
) -> EvaluationMetrics:
    """
    Calculate Top-1, Top-3 and Top-5 accuracy for a repository evaluation.
    """

    metrics = EvaluationMetrics()

    metrics.total_issues = sum(
        1 for record in evaluation.records if record.actual_pull_request is not None
    )

    for record in evaluation.records:
        actual = record.actual_pull_request
        predictions = sorted(
            record.predictions,
            key=lambda prediction: prediction.rank,
        )

        predicted = predictions[0].pull_request_number if predictions else None

        if actual is not None:
            if predicted == actual:
                metrics.true_positive += 1
            elif predicted is None:
                metrics.false_negative += 1
            else:
                metrics.false_positive += 1
                metrics.false_negative += 1

        if actual is None:
            continue

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
