from issuescout.models.analysis import (
    RelationPrediction,
)

from issuescout.models.issue import Issue
from issuescout.models.pull_request import PullRequest

from issuescout.scanner.relation import RelationEngine
from issuescout.scanner.relation.weights import (
    STRONG_EVIDENCE_ANALYZERS,
    STRONG_EVIDENCE_BONUS,
)


class AnalysisService:
    def __init__(
        self,
        relation_engine: RelationEngine,
    ):
        self.relation_engine = relation_engine

    async def analyze(
        self,
        issue: Issue,
        pull_requests: list[PullRequest],
    ) -> list[RelationPrediction]:

        predictions: list[RelationPrediction] = []

        for pull_request in pull_requests:
            score, results = await self.relation_engine.analyze(
                issue,
                pull_request,
            )

            strong_evidence = any(
                result.analyzer in STRONG_EVIDENCE_ANALYZERS for result in results
            )

            if strong_evidence:
                score += STRONG_EVIDENCE_BONUS

            predictions.append(
                RelationPrediction(
                    pull_request=pull_request,
                    score=score,
                    results=results,
                    strong_evidence=strong_evidence,
                )
            )

        return predictions
