from __future__ import annotations

from issuescout.models import (
    Issue,
    PullRequest,
)
from issuescout.models.analysis import PredictionResult
from issuescout.prediction.prediction_service import PredictionService


class ApplicationPredictionService:
    """
    Application service for prediction operations.

    This layer isolates API and CLI clients from the prediction
    implementation.
    """

    def __init__(
        self,
        prediction: PredictionService,
    ) -> None:
        self._prediction = prediction

    async def predict(
        self,
        issue: Issue,
        pull_requests: list[PullRequest],
        *,
        verbose: bool = False,
    ) -> PredictionResult:
        return await self._prediction.predict(
            issue,
            pull_requests,
            verbose=verbose,
        )
