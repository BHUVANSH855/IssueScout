from issuescout.models import (
    RelationPrediction,
)

from issuescout.output.explanation import (
    explain_prediction,
)

from issuescout.scanner.relation.result import (
    RelationResult,
)

from tests.helpers.factories import (
    make_pull_request,
)


def make_result(
    score: int,
    reason: str,
):
    return RelationResult(
        analyzer="test",
        score=score,
        confidence=100,
        reason=reason,
    )


def test_returns_all_positive_reasons():
    prediction = RelationPrediction(
        pull_request=make_pull_request(),
        score=100,
        results=[
            make_result(10, "Title matched"),
            make_result(20, "Author matched"),
        ],
    )

    assert explain_prediction(
        prediction,
    ) == [
        "Title matched",
        "Author matched",
    ]


def test_ignores_zero_scores():
    prediction = RelationPrediction(
        pull_request=make_pull_request(),
        score=100,
        results=[
            make_result(10, "Keep"),
            make_result(0, "Ignore"),
        ],
    )

    assert explain_prediction(
        prediction,
    ) == [
        "Keep",
    ]


def test_ignores_negative_scores():
    prediction = RelationPrediction(
        pull_request=make_pull_request(),
        score=100,
        results=[
            make_result(-10, "Ignore"),
            make_result(5, "Keep"),
        ],
    )

    assert explain_prediction(
        prediction,
    ) == [
        "Keep",
    ]


def test_returns_empty_list_when_no_positive_results():
    prediction = RelationPrediction(
        pull_request=make_pull_request(),
        score=0,
        results=[
            make_result(0, "Zero"),
            make_result(-5, "Negative"),
        ],
    )

    assert (
        explain_prediction(
            prediction,
        )
        == []
    )
