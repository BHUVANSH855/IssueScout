from issuescout.models.analysis import PredictionResult


class ConsoleReporter:
    def report(
        self,
        result: PredictionResult,
    ) -> None:

        if result.prediction is None:
            print("No prediction.")
            return

        print("=" * 100)
        print("Candidate Ranking")

        for candidate in result.candidates:
            print(f"PR #{candidate.pull_request.number} -> {candidate.score}")

        print("=" * 100)

        print(f"Best candidate: PR #{result.prediction.pull_request.number}")

        print(f"Score: {result.prediction.score}")

        print(f"Confidence: {result.confidence}")

        print("Prediction accepted" if result.accepted else "Prediction rejected")

        print()

        print("Evidence:")

        for evidence in result.evidence:
            print(f"- {evidence.reason}")
