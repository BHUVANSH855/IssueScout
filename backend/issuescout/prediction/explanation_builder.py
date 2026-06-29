from __future__ import annotations

from issuescout.models import (
    ExplanationItem,
    PredictionExplanation,
)


class ExplanationBuilder:
    """
    Builds a structured explanation for a prediction.
    """

    def build(
        self,
        *,
        pull_request_number: int,
        total_score: int,
        confidence: str,
        items: list[ExplanationItem],
    ) -> PredictionExplanation:

        summary = (
            f"Predicted PR #{pull_request_number} "
            f"using {len(items)} evidence item"
            f"{'' if len(items) == 1 else 's'}."
        )

        return PredictionExplanation(
            summary=summary,
            confidence=confidence,
            total_score=total_score,
            items=items,
        )
