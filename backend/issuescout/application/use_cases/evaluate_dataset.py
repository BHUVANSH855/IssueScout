from __future__ import annotations

from pathlib import Path

from issuescout.application.evaluation_service import (
    ApplicationEvaluationService,
)
from issuescout.evaluation.metrics.summary import (
    EvaluationSummary,
)


class EvaluateDatasetUseCase:
    """
    Executes evaluation of a dataset.
    """

    def __init__(
        self,
        service: ApplicationEvaluationService,
    ) -> None:
        self._service = service

    def execute(
        self,
        dataset: str | Path,
    ) -> EvaluationSummary:
        return self._service.evaluate_dataset(
            dataset,
        )
