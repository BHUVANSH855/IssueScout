from issuescout.models.analysis import (
    RelationPrediction,
)

from issuescout.ranking import Ranker

from tests.helpers.factories import (
    make_pull_request,
)


def prediction(
    number: int,
    score: int,
) -> RelationPrediction:

    return RelationPrediction(
        pull_request=make_pull_request(
            number=number,
        ),
        score=score,
        results=[],
        strong_evidence=False,
    )


def test_rank_descending():

    ranker = Ranker()

    ranked = ranker.rank(
        [
            prediction(1, 40),
            prediction(2, 90),
            prediction(3, 60),
        ]
    )

    assert [p.pull_request.number for p in ranked] == [
        2,
        3,
        1,
    ]


def test_best_returns_highest_score():

    ranker = Ranker()

    best = ranker.best(
        [
            prediction(1, 20),
            prediction(2, 95),
            prediction(3, 80),
        ]
    )

    assert best is not None
    assert best.pull_request.number == 2


def test_best_empty_list():

    ranker = Ranker()

    assert ranker.best([]) is None


def test_rank_single_prediction():

    ranker = Ranker()

    ranked = ranker.rank(
        [
            prediction(
                1,
                42,
            ),
        ]
    )

    assert len(ranked) == 1
    assert ranked[0].score == 42


def test_rank_preserves_equal_scores():

    ranker = Ranker()

    predictions = [
        prediction(1, 50),
        prediction(2, 50),
        prediction(3, 50),
    ]

    ranked = ranker.rank(
        predictions,
    )

    assert [p.pull_request.number for p in ranked] == [
        1,
        2,
        3,
    ]


def test_best_single_prediction():

    ranker = Ranker()

    best = ranker.best(
        [
            prediction(
                5,
                77,
            ),
        ]
    )

    assert best is not None
    assert best.pull_request.number == 5
