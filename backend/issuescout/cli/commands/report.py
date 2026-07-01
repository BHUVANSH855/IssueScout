from __future__ import annotations

from issuescout.evaluation.report import EvaluationReport


def report(
    repository: str,
) -> EvaluationReport:
    """
    Create an empty evaluation report for a repository.

    The report can later be populated by the evaluation pipeline.
    """

    return EvaluationReport(
        repository=repository,
    )
