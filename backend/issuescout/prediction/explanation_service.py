from issuescout.models.analysis import (
    RelationPrediction,
)

from issuescout.models.explanation import (
    ExplanationItem,
)


class ExplanationService:
    """
    Extracts positive evidence from a relation prediction.
    """

    def build(
        self,
        prediction: RelationPrediction,
    ) -> list[ExplanationItem]:

        explanation = []

        for result in prediction.results:
            if result.score <= 0:
                continue

            explanation.append(
                ExplanationItem(
                    analyzer=result.analyzer,
                    score=result.score,
                    confidence=result.confidence,
                    reason=result.reason,
                    evidence_type=result.evidence_type,
                )
            )

        return explanation
