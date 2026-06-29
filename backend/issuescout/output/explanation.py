from issuescout.models.analysis import (
    RelationPrediction,
)


def explain_prediction(
    prediction: RelationPrediction,
) -> list[str]:

    return [result.reason for result in prediction.results if result.score > 0]
