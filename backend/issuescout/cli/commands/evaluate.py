from __future__ import annotations

from pathlib import Path

from issuescout.evaluation.loader import EvaluationLoader
from issuescout.evaluation.pipeline import EvaluationPipeline
from issuescout.evaluation.runner import EvaluationRunner
from issuescout.evaluation.metrics.summary import EvaluationSummary


class EvaluationCommand:
    """
    High-level entry point for IssueScout evaluation.

    Workflow
    --------
        Dataset
           │
           ▼
      EvaluationLoader
           │
           ▼
      EvaluationRunner
           │
           ▼
      EvaluationPipeline
           │
           ▼
      EvaluationSummary
    """

    def __init__(self) -> None:
        self._loader = EvaluationLoader()
        self._runner = EvaluationRunner()
        self._pipeline = EvaluationPipeline()

    def evaluate(
        self,
        dataset: str | Path,
    ) -> EvaluationSummary:
        """
        Evaluate a dataset and return an evaluation summary.
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


def evaluate() -> EvaluationCommand:
    """
    Create an evaluation command.

    Keeping this factory preserves backward compatibility while allowing
    the command implementation to evolve independently.
    """

    return EvaluationCommand()
