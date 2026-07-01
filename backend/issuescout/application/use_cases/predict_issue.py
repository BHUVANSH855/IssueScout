from __future__ import annotations

from issuescout.application.prediction_service import (
    ApplicationPredictionService,
)
from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.models.analysis import PredictionResult


class PredictIssueUseCase:
    """
    Executes prediction for a single issue.
    """

    def __init__(
        self,
        service: ApplicationPredictionService,
    ) -> None:
        self._service = service

    async def execute(
        self,
        issue: Issue,
        pull_requests: list[PullRequest],
        *,
        verbose: bool = False,
    ) -> PredictionResult:
        return await self._service.predict(
            issue,
            pull_requests,
            verbose=verbose,
        )
