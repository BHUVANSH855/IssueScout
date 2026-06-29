from issuescout.models import (
    PullRequest,
    RepositoryScanContext,
)

from issuescout.scanner.detectors.linked_pr_detector import (
    LinkedPRDetector,
)

from issuescout.prediction import (
    PredictionService,
)

from issuescout.evidence import (
    EvidenceCollector,
)

from issuescout.scanner.relation import (
    RelationEngine,
)

from issuescout.scanner.relation.registry import (
    default_analyzers,
)

from issuescout.presentation import (
    ConsoleReporter,
)


class GitHubLinkedPRDetector(LinkedPRDetector):
    """
    Detect linked pull requests using the
    already-fetched RepositoryScanContext.
    """

    def __init__(
        self,
        evidence_collector: EvidenceCollector | None = None,
        prediction_service: PredictionService | None = None,
        console_reporter: ConsoleReporter | None = None,
        relation_engine: RelationEngine | None = None,
    ):
        self.evidence_collector = evidence_collector or EvidenceCollector()

        self.relation_engine = relation_engine or RelationEngine(
            default_analyzers(),
        )

        self.prediction_service = prediction_service or PredictionService(
            self.relation_engine,
        )

        self.console_reporter = console_reporter or ConsoleReporter()

    async def find_linked_pr(
        self,
        context: RepositoryScanContext,
        issue_number: int,
    ) -> PullRequest | None:

        issue = next(issue for issue in context.issues if issue.number == issue_number)

        await self.evidence_collector.collect(
            context,
            issue,
        )

        prediction = await self.prediction_service.predict(
            issue,
            context.pull_requests,
        )

        if prediction.prediction is None:
            return None

        self.console_reporter.report(
            prediction,
        )

        return prediction.prediction.pull_request

    async def close(self):
        await self.evidence_collector.close()
