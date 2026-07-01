from __future__ import annotations

from issuescout.application.evaluation_service import (
    ApplicationEvaluationService,
)
from issuescout.application.prediction_service import (
    ApplicationPredictionService,
)
from issuescout.application.repository_service import (
    ApplicationRepositoryService,
)
from issuescout.application.scan_service import (
    ApplicationScanService,
)
from issuescout.evaluation.loader import EvaluationLoader
from issuescout.evaluation.pipeline import EvaluationPipeline
from issuescout.evaluation.runner import EvaluationRunner
from issuescout.prediction.prediction_service import PredictionService
from issuescout.scanner.engine import ScannerEngine
from issuescout.scanner.relation import RelationEngine
from issuescout.services.repository_service import RepositoryService


class ApplicationContainer:
    """
    Central dependency container for the IssueScout application.

    The container owns shared infrastructure objects and exposes
    high-level application services to the API, CLI, and future UI.
    """

    def __init__(self) -> None:
        #
        # Shared infrastructure
        #
        self._relation_engine = RelationEngine()

        self._scanner_engine = ScannerEngine()

        self._repository_service = RepositoryService()

        self._prediction_engine = PredictionService(
            relation_engine=self._relation_engine,
        )

        self._evaluation_runner = EvaluationRunner()

        self._evaluation_loader = EvaluationLoader()

        self._evaluation_pipeline = EvaluationPipeline()

        #
        # Application services
        #
        self._repository = ApplicationRepositoryService(
            self._repository_service,
        )

        self._scanner = ApplicationScanService(
            self._scanner_engine,
        )

        self._prediction = ApplicationPredictionService(
            self._prediction_engine,
        )

        self._evaluation = ApplicationEvaluationService(
            runner=self._evaluation_runner,
            loader=self._evaluation_loader,
            pipeline=self._evaluation_pipeline,
        )

    @property
    def repository(
        self,
    ) -> ApplicationRepositoryService:
        return self._repository

    @property
    def scanner(
        self,
    ) -> ApplicationScanService:
        return self._scanner

    @property
    def prediction(
        self,
    ) -> ApplicationPredictionService:
        return self._prediction

    @property
    def evaluation(
        self,
    ) -> ApplicationEvaluationService:
        return self._evaluation
