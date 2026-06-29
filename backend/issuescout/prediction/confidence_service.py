from issuescout.models.analysis import (
    RelationPrediction,
)


class ConfidenceService:
    """
    Determines the user-facing confidence
    for a prediction based on the evidence
    produced by the relation engine.
    """

    def confidence(
        self,
        prediction: RelationPrediction,
    ) -> str:

        strong = sum(
            1
            for result in prediction.results
            if (result.score > 0 and result.evidence_type == "strong")
        )

        supporting = sum(
            1
            for result in prediction.results
            if (result.score > 0 and result.evidence_type == "supporting")
        )

        if strong >= 2:
            return "Very High"

        if strong == 1:
            return "High"

        if supporting >= 4:
            return "Medium"

        if supporting >= 2:
            return "Low"

        return "Very Low"
