from issuescout.scanner.relation.metadata import (
    AnalyzerMetadata,
)


class ScoringPolicy:
    """
    Centralized scoring rules for analyzers.
    """

    def score(
        self,
        metadata: AnalyzerMetadata,
        confidence: int,
    ) -> int:

        if confidence <= 0:
            return 0

        return round(metadata.weight * confidence / 100)
