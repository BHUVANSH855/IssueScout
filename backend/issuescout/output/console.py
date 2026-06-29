from issuescout.models.analysis import PredictionResult


class ConsoleFormatter:
    def display(
        self,
        prediction: PredictionResult,
    ) -> None:

        if prediction.prediction is None:
            print("No prediction available.")
            return

        print("=" * 100)
        print("Candidate Ranking")

        for candidate in prediction.candidates:
            print(f"PR #{candidate.pull_request.number} -> {candidate.score}")

        print("=" * 100)

        print(f"Best candidate: PR #{prediction.prediction.pull_request.number}")

        print(f"Score: {prediction.prediction.score}")

        print(f"Confidence: {prediction.confidence}")

        if prediction.accepted:
            print(f"Prediction accepted (score >= {prediction.threshold})")

        else:
            print(f"Prediction rejected (score below {prediction.threshold})")
