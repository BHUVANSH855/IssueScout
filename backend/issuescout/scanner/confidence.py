from issuescout.models import AnalysisResult


class ConfidenceCalculator:
    def calculate(
        self,
        results: list[AnalysisResult],
    ) -> int:
        if not results:
            return 0

        confidence = sum(result.score for result in results if result.passed)

        return max(0, min(confidence, 100))
