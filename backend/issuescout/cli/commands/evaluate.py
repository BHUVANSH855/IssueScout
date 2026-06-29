from __future__ import annotations

from issuescout.evaluation.evaluator import Evaluator
from issuescout.evaluation.models import RepositoryEvaluation


def run() -> None:
    """
    Run the evaluation pipeline.
    """

    evaluator = Evaluator()

    evaluation = RepositoryEvaluation(
        repository="demo",
    )

    summary = evaluator.evaluate(
        evaluation,
    )

    metrics = summary.metrics

    print()
    print("=" * 60)
    print("IssueScout Evaluation")
    print("=" * 60)
    print(f"Repository      : {summary.repository}")
    print(f"Total Issues    : {metrics.total_issues}")
    print(f"Top-1 Accuracy  : {metrics.top1_accuracy:.2f}%")
    print(f"Top-3 Accuracy  : {metrics.top3_accuracy:.2f}%")
    print(f"Top-5 Accuracy  : {metrics.top5_accuracy:.2f}%")
    print(f"Precision       : {metrics.precision:.2f}%")
    print(f"Recall          : {metrics.recall:.2f}%")
    print(f"F1 Score        : {metrics.f1_score:.2f}%")
    print("=" * 60)
