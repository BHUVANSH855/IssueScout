from issuescout.scanner.relation.metadata import (
    AnalyzerMetadata,
)

from issuescout.scanner.relation.scoring import (
    ScoringPolicy,
)


def metadata(
    weight: int,
):

    return AnalyzerMetadata(
        name="test",
        weight=weight,
    )


def test_zero_confidence():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(20),
            0,
        )
        == 0
    )


def test_negative_confidence():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(20),
            -10,
        )
        == 0
    )


def test_half_confidence():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(20),
            50,
        )
        == 10
    )


def test_full_confidence():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(20),
            100,
        )
        == 20
    )


def test_rounding():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(25),
            33,
        )
        == 8
    )


def test_small_weight():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(5),
            80,
        )
        == 4
    )


def test_zero_weight():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(0),
            100,
        )
        == 0
    )


def test_large_weight():

    scoring = ScoringPolicy()

    assert (
        scoring.score(
            metadata(50),
            60,
        )
        == 30
    )
