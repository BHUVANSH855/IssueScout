from issuescout.models.analysis import PredictionResult

from issuescout.prediction.explanation_metadata import (
    EXPLANATION_METADATA,
)


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
        print("=" * 100)

        for candidate in prediction.candidates:
            print(f"PR #{candidate.pull_request.number} -> {candidate.score}")

        print()

        print("=" * 100)
        print("Prediction")
        print("=" * 100)

        # Keep legacy output for compatibility with tests.
        print(f"Best candidate: PR #{prediction.prediction.pull_request.number}")

        print(f"Score: {prediction.prediction.score}")

        print(f"Confidence: {prediction.confidence}")

        # Additional information.
        print(f"Issue          : #{prediction.issue_number}")

        print(f"Predicted PR   : #{prediction.prediction.pull_request.number}")

        print(f"Threshold      : {prediction.threshold}")

        print()

        if prediction.accepted:
            print(f"Prediction accepted (score >= {prediction.threshold})")
        else:
            print(f"Prediction rejected (score below {prediction.threshold})")

        if prediction.explanation is not None:
            print()
            print("=" * 100)
            print("Evidence")
            print("=" * 100)

            for item in prediction.explanation.items:
                metadata = EXPLANATION_METADATA.get(
                    item.analyzer,
                )

                if metadata is None:
                    title = item.analyzer.replace(
                        "_",
                        " ",
                    ).title()
                    category = "Other"
                else:
                    title = metadata.title
                    category = metadata.category

                print(title)
                print(f"  Category : {category}")
                print(f"  Score    : +{item.score}")
                print(f"  Reason   : {item.reason}")
                print()

            print("=" * 100)
            print("Summary")
            print("=" * 100)

            print(
                prediction.explanation.summary,
            )

        print("=" * 100)
