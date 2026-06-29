from __future__ import annotations

import asyncio

from .config import (
    MAX_STRONG_EVIDENCE_SCORE,
    MAX_SUPPORTING_EVIDENCE_SCORE,
)
from .result import RelationResult


class RelationEngine:
    def __init__(
        self,
        analyzers,
    ):
        self.analyzers = analyzers

    def confidence_level(
        self,
        score: int,
    ) -> str:

        if score >= 90:
            return "Very High"

        if score >= 70:
            return "High"

        if score >= 50:
            return "Medium"

        if score >= 30:
            return "Low"

        return "Very Low"

    async def analyze(
        self,
        issue,
        pull_request,
    ):

        results: list[RelationResult] = await asyncio.gather(
            *[
                analyzer.analyze(
                    issue,
                    pull_request,
                )
                for analyzer in self.analyzers
            ]
        )

        strong_score = 0
        supporting_score = 0

        for result in results:
            score = max(
                result.score,
                0,
            )

            if result.evidence_type == "strong":
                strong_score += score
            else:
                supporting_score += score

        strong_score = min(
            strong_score,
            MAX_STRONG_EVIDENCE_SCORE,
        )

        supporting_score = min(
            supporting_score,
            MAX_SUPPORTING_EVIDENCE_SCORE,
        )

        total_score = strong_score + supporting_score

        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return total_score, results
