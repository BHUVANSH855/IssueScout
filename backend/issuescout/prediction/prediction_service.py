from issuescout.models.analysis import (
    PredictionResult,
    RelationPrediction,
)

from issuescout.models.issue import Issue
from issuescout.models.pull_request import PullRequest
from issuescout.ranking import Ranker
from issuescout.scanner.relation import RelationEngine
from issuescout.scanner.relation.config import (
    DEFAULT_THRESHOLD,
)

from issuescout.prediction.analysis_service import (
    AnalysisService,
)
from issuescout.prediction.explanation_service import (
    ExplanationService,
)
from issuescout.prediction.confidence_service import (
    ConfidenceService,
)


class PredictionService:
    def __init__(
        self,
        relation_engine: RelationEngine,
    ):
        self.relation_engine = relation_engine
        self.analysis_service = AnalysisService(
            relation_engine,
        )
        self.ranker = Ranker()
        self.confidence_service = ConfidenceService()
        self.explanation_service = ExplanationService()

    def _sort_predictions(
        self,
        predictions: list[RelationPrediction],
    ) -> list[RelationPrediction]:

        return self.ranker.rank(
            predictions,
        )

    def _best_prediction(
        self,
        predictions: list[RelationPrediction],
    ) -> RelationPrediction | None:

        return self.ranker.best(
            predictions,
        )

    def _evidence(
        self,
        prediction: RelationPrediction,
    ):

        return [result for result in prediction.results if result.score > 0]

    async def predict(
        self,
        issue: Issue,
        pull_requests: list[PullRequest],
        *,
        verbose: bool = False,
    ) -> PredictionResult:

        predictions = await self.analysis_service.analyze(
            issue,
            pull_requests,
        )

        predictions = self._sort_predictions(
            predictions,
        )

        result = PredictionResult(
            issue_number=issue.number,
            candidates=predictions,
            threshold=DEFAULT_THRESHOLD,
        )

        best = self._best_prediction(
            predictions,
        )

        if best is None:
            return result

        result.prediction = best

        result.confidence = self.confidence_service.confidence(
            best,
        )

        result.accepted = best.score >= DEFAULT_THRESHOLD

        result.evidence = self._evidence(best)

        result.explanation = self.explanation_service.build(
            best,
        )

        return result
