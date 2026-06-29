from issuescout.models.analysis import (
    RelationPrediction,
)
from issuescout.scanner.relation.result import (
    RelationResult,
)
from issuescout.prediction.confidence_service import (
    ConfidenceService,
)

from tests.helpers.factories import (
    make_pull_request,
)


def make_result(
    score: int,
    evidence_type: str,
) -> RelationResult:

    return RelationResult(
        analyzer="test",
        score=score,
        confidence=100,
        reason="test",
        evidence_type=evidence_type,
    )


def make_prediction(results):

    return RelationPrediction(
        pull_request=make_pull_request(),
        score=0,
        results=results,
    )


def test_very_high_confidence():

    prediction = make_prediction(
        [
            make_result(10, "strong"),
            make_result(20, "strong"),
        ]
    )

    service = ConfidenceService()

    assert (
        service.confidence(prediction)
        == "Very High"
    )


def test_high_confidence():

    prediction = make_prediction(
        [
            make_result(10, "strong"),
            make_result(5, "supporting"),
        ]
    )

    service = ConfidenceService()

    assert (
        service.confidence(prediction)
        == "High"
    )


def test_medium_confidence():

    prediction = make_prediction(
        [
            make_result(5, "supporting"),
            make_result(5, "supporting"),
            make_result(5, "supporting"),
            make_result(5, "supporting"),
        ]
    )

    service = ConfidenceService()

    assert (
        service.confidence(prediction)
        == "Medium"
    )


def test_low_confidence():

    prediction = make_prediction(
        [
            make_result(5, "supporting"),
            make_result(5, "supporting"),
        ]
    )

    service = ConfidenceService()

    assert (
        service.confidence(prediction)
        == "Low"
    )


def test_very_low_confidence():

    prediction = make_prediction(
        [
            make_result(0, "supporting"),
        ]
    )

    service = ConfidenceService()

    assert (
        service.confidence(prediction)
        == "Very Low"
    )