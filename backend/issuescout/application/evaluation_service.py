from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from issuescout.evaluation.comparison.result import ComparisonResult
from issuescout.evaluation.loader import EvaluationLoader
from issuescout.evaluation.metrics.summary import EvaluationSummary
from issuescout.evaluation.pipeline import EvaluationPipeline
from issuescout.evaluation.runner import EvaluationRunner
from issuescout.evaluation.models import EvaluationRecord


class ApplicationEvaluationService:
    """
    Application service for evaluation operations.

    Coordinates dataset loading, evaluation execution,
    and metric summarization while delegating the actual
    work to the evaluation subsystem.
    """

    def __init__(
        self,
        runner: EvaluationRunner | None = None,
        loader: EvaluationLoader | None = None,
        pipeline: EvaluationPipeline | None = None,
    ) -> None:
        self._runner = runner or EvaluationRunner()
        self._loader = loader or EvaluationLoader()
        self._pipeline = pipeline or EvaluationPipeline()

    def evaluate_dataset(
        self,
        dataset: str | Path,
    ) -> EvaluationSummary:
        """
        Load and evaluate a dataset.
        """
        repository = self._loader.load(
            dataset,
        )

        comparisons = self._runner.run(
            repository.records,
        )

        return self._pipeline.summarize(
            comparisons,
        )

    def summarize(
        self,
        records: Iterable[EvaluationRecord],
    ) -> EvaluationSummary:
        """
        Evaluate an in-memory collection of evaluation records.
        """
        comparisons: list[ComparisonResult] = self._runner.run(
            records,
        )

        return self._pipeline.summarize(
            comparisons,
        )
