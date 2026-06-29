import pytest

from issuescout.models.analysis import (
    RelationPrediction,
)

from issuescout.prediction.prediction_service import (
    PredictionService,
)

from issuescout.scanner.relation.result import (
    RelationResult,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


class FakeRelationEngine:
    pass


def make_prediction(
    pull_request,
    score,
    evidence_type="strong",
):

    return RelationPrediction(
        pull_request=pull_request,
        score=score,
        results=[
            RelationResult(
                analyzer="test",
                score=score,
                confidence=100,
                reason="matched",
                evidence_type=evidence_type,
            )
        ],
    )


@pytest.mark.anyio
async def test_predict_returns_best_candidate():

    service = PredictionService(
        FakeRelationEngine(),
    )

    pr1 = make_pull_request(
        number=1,
    )

    pr2 = make_pull_request(
        number=2,
    )

    predictions = [
        make_prediction(
            pr1,
            30,
        ),
        make_prediction(
            pr2,
            90,
        ),
    ]

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return predictions

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [pr1, pr2],
    )

    assert result.prediction.pull_request.number == 2


@pytest.mark.anyio
async def test_predict_returns_sorted_candidates():

    service = PredictionService(
        FakeRelationEngine(),
    )

    pr1 = make_pull_request(
        number=1,
    )

    pr2 = make_pull_request(
        number=2,
    )

    predictions = [
        make_prediction(
            pr1,
            10,
        ),
        make_prediction(
            pr2,
            80,
        ),
    ]

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return predictions

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [pr1, pr2],
    )

    assert result.candidates[0].score >= result.candidates[1].score


@pytest.mark.anyio
async def test_predict_accepts_high_score():

    service = PredictionService(
        FakeRelationEngine(),
    )

    pr = make_pull_request()

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return [
            make_prediction(
                pr,
                100,
            )
        ]

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [pr],
    )

    assert result.accepted is True


@pytest.mark.anyio
async def test_predict_rejects_low_score():

    service = PredictionService(
        FakeRelationEngine(),
    )

    pr = make_pull_request()

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return [
            make_prediction(
                pr,
                1,
            )
        ]

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [pr],
    )

    assert result.accepted is False


@pytest.mark.anyio
async def test_predict_returns_no_prediction_when_empty():

    service = PredictionService(
        FakeRelationEngine(),
    )

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return []

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [],
    )

    assert result.prediction is None
    assert result.candidates == []


@pytest.mark.anyio
async def test_predict_collects_positive_evidence():

    service = PredictionService(
        FakeRelationEngine(),
    )

    pr = make_pull_request()

    prediction = RelationPrediction(
        pull_request=pr,
        score=80,
        results=[
            RelationResult(
                analyzer="positive",
                score=20,
                confidence=100,
                reason="good",
                evidence_type="strong",
            ),
            RelationResult(
                analyzer="negative",
                score=0,
                confidence=0,
                reason="none",
                evidence_type="supporting",
            ),
        ],
    )

    async def fake_analyze(
        issue,
        pull_requests,
    ):
        return [prediction]

    service.analysis_service.analyze = fake_analyze

    result = await service.predict(
        make_issue(),
        [pr],
    )

    assert len(result.evidence) == 1
    assert result.evidence[0].analyzer == "positive"
