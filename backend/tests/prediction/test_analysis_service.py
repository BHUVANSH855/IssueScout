import pytest

from issuescout.prediction.analysis_service import (
    AnalysisService,
)

from issuescout.scanner.relation.result import (
    RelationResult,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


class FakeRelationEngine:
    def __init__(
        self,
        responses,
    ):
        self.responses = responses
        self.calls = 0

    async def analyze(
        self,
        issue,
        pull_request,
    ):
        response = self.responses[self.calls]
        self.calls += 1
        return response


def make_result(
    analyzer,
    score,
    evidence_type="supporting",
):

    return RelationResult(
        analyzer=analyzer,
        score=score,
        confidence=100 if score else 0,
        reason="test",
        evidence_type=evidence_type,
    )


@pytest.mark.anyio
async def test_returns_prediction_for_each_pr():

    engine = FakeRelationEngine(
        [
            (
                25,
                [],
            ),
            (
                60,
                [],
            ),
        ]
    )

    service = AnalysisService(
        engine,
    )

    predictions = await service.analyze(
        make_issue(),
        [
            make_pull_request(
                number=1,
            ),
            make_pull_request(
                number=2,
            ),
        ],
    )

    assert len(predictions) == 2


@pytest.mark.anyio
async def test_preserves_scores_without_bonus():

    engine = FakeRelationEngine(
        [
            (
                42,
                [
                    make_result(
                        "title_similarity",
                        42,
                    )
                ],
            ),
        ]
    )

    service = AnalysisService(
        engine,
    )

    prediction = (
        await service.analyze(
            make_issue(),
            [
                make_pull_request(),
            ],
        )
    )[0]

    assert prediction.score == 42
    assert prediction.strong_evidence is False


@pytest.mark.anyio
async def test_adds_bonus_for_strong_evidence():

    engine = FakeRelationEngine(
        [
            (
                50,
                [
                    make_result(
                        "body_reference",
                        40,
                        "strong",
                    )
                ],
            ),
        ]
    )

    service = AnalysisService(
        engine,
    )

    prediction = (
        await service.analyze(
            make_issue(),
            [
                make_pull_request(),
            ],
        )
    )[0]

    assert prediction.strong_evidence is True
    assert prediction.score > 50


@pytest.mark.anyio
async def test_results_are_preserved():

    results = [
        make_result(
            "title_similarity",
            20,
        ),
        make_result(
            "author_similarity",
            10,
        ),
    ]

    engine = FakeRelationEngine(
        [
            (
                30,
                results,
            ),
        ]
    )

    service = AnalysisService(
        engine,
    )

    prediction = (
        await service.analyze(
            make_issue(),
            [
                make_pull_request(),
            ],
        )
    )[0]

    assert prediction.results == results


@pytest.mark.anyio
async def test_empty_pull_request_list():

    engine = FakeRelationEngine(
        [],
    )

    service = AnalysisService(
        engine,
    )

    predictions = await service.analyze(
        make_issue(),
        [],
    )

    assert predictions == []


@pytest.mark.anyio
async def test_engine_called_once_per_pr():

    engine = FakeRelationEngine(
        [
            (
                1,
                [],
            ),
            (
                2,
                [],
            ),
            (
                3,
                [],
            ),
        ]
    )

    service = AnalysisService(
        engine,
    )

    await service.analyze(
        make_issue(),
        [
            make_pull_request(
                number=1,
            ),
            make_pull_request(
                number=2,
            ),
            make_pull_request(
                number=3,
            ),
        ],
    )

    assert engine.calls == 3
