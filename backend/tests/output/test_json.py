from issuescout.models import (
    PredictionResult,
)
from issuescout.output.json import JsonFormatter


def test_returns_dictionary():
    prediction = PredictionResult(
        issue_number=123,
    )

    formatter = JsonFormatter()

    result = formatter.format(
        prediction,
    )

    assert isinstance(
        result,
        dict,
    )


def test_contains_prediction_fields():
    prediction = PredictionResult(
        issue_number=123,
        accepted=True,
        confidence="High",
        threshold=75,
    )

    formatter = JsonFormatter()

    result = formatter.format(
        prediction,
    )

    assert result["issue_number"] == 123
    assert result["accepted"] is True
    assert result["confidence"] == "High"
    assert result["threshold"] == 75


def test_matches_model_dump():
    prediction = PredictionResult(
        issue_number=456,
    )

    formatter = JsonFormatter()

    assert formatter.format(
        prediction,
    ) == prediction.model_dump()