from issuescout.models import AnalysisResult


class ConfidenceCalculator:
    def calculate(
        self,
        results: list[AnalysisResult],
    ) -> int:
        return sum(result.score for result in results if result.passed)
