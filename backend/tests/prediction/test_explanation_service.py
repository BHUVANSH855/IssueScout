from issuescout.models.analysis import (
    RelationPrediction,
)

from issuescout.models.explanation import (
    ExplanationItem,
)

from issuescout.prediction.explanation_service import (
    ExplanationService,
)

from issuescout.scanner.relation.result import (
    RelationResult,
)

from tests.helpers.factories import (
    make_pull_request,
)


def make_result(
    analyzer: str,
    score: int,
    confidence: int = 100,
    evidence_type: str = "supporting",
):

    return RelationResult(
        analyzer=analyzer,
        score=score,
        confidence=confidence,
        reason=f"{analyzer} matched",
        evidence_type=evidence_type,
    )


def make_prediction(results):

    return RelationPrediction(
        pull_request=make_pull_request(),
        score=0,
        results=results,
    )


def test_build_returns_only_positive_results():

    prediction = make_prediction(
        [
            make_result(
                "title_similarity",
                25,
            ),
            make_result(
                "author_similarity",
                0,
            ),
            make_result(
                "body_reference",
                40,
                evidence_type="strong",
            ),
        ]
    )

    explanation = ExplanationService().build(
        prediction,
    )

    assert len(explanation) == 2


def test_build_preserves_fields():

    prediction = make_prediction(
        [
            make_result(
                analyzer="title_similarity",
                score=18,
                confidence=72,
                evidence_type="supporting",
            )
        ]
    )

    item = ExplanationService().build(
        prediction,
    )[0]

    assert isinstance(
        item,
        ExplanationItem,
    )

    assert item.analyzer == "title_similarity"
    assert item.score == 18
    assert item.confidence == 72
    assert item.reason == "title_similarity matched"
    assert item.evidence_type == "supporting"


def test_build_returns_empty_when_no_positive_results():

    prediction = make_prediction(
        [
            make_result(
                "title_similarity",
                0,
            ),
            make_result(
                "body_reference",
                0,
            ),
        ]
    )

    explanation = ExplanationService().build(
        prediction,
    )

    assert explanation == []


def test_build_keeps_result_order():

    prediction = make_prediction(
        [
            make_result(
                "body_reference",
                40,
            ),
            make_result(
                "title_similarity",
                20,
            ),
            make_result(
                "label_similarity",
                10,
            ),
        ]
    )

    explanation = ExplanationService().build(
        prediction,
    )

    assert [item.analyzer for item in explanation] == [
        "body_reference",
        "title_similarity",
        "label_similarity",
    ]


def test_build_multiple_evidence_types():

    prediction = make_prediction(
        [
            make_result(
                "body_reference",
                40,
                evidence_type="strong",
            ),
            make_result(
                "title_similarity",
                20,
                evidence_type="supporting",
            ),
        ]
    )

    explanation = ExplanationService().build(
        prediction,
    )

    assert explanation[0].evidence_type == "strong"
    assert explanation[1].evidence_type == "supporting"
