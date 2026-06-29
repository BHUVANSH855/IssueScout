from issuescout.models import (
    PredictionResult,
    RelationPrediction,
)

from issuescout.output.console import (
    ConsoleFormatter,
)

from issuescout.scanner.relation.result import (
    RelationResult,
)

from tests.helpers.factories import (
    make_pull_request,
)


def make_prediction(
    *,
    accepted: bool = True,
):
    relation = RelationPrediction(
        pull_request=make_pull_request(
            number=42,
            title="Fix login bug",
        ),
        score=90,
        results=[
            RelationResult(
                analyzer="title",
                score=90,
                confidence=100,
                reason="Title matched",
            ),
        ],
    )

    return PredictionResult(
        issue_number=123,
        prediction=relation,
        candidates=[relation],
        accepted=accepted,
        threshold=75,
        confidence="High",
    )


def test_displays_no_prediction_message(
    capsys,
):
    formatter = ConsoleFormatter()

    formatter.display(
        PredictionResult(
            issue_number=1,
        )
    )

    captured = capsys.readouterr()

    assert "No prediction available." in captured.out


def test_displays_candidate_ranking(
    capsys,
):
    formatter = ConsoleFormatter()

    formatter.display(
        make_prediction(),
    )

    output = capsys.readouterr().out

    assert "Candidate Ranking" in output
    assert "PR #42 -> 90" in output


def test_displays_prediction_details(
    capsys,
):
    formatter = ConsoleFormatter()

    formatter.display(
        make_prediction(),
    )

    output = capsys.readouterr().out

    assert "Best candidate: PR #42" in output
    assert "Score: 90" in output
    assert "Confidence: High" in output


def test_displays_prediction_accepted(
    capsys,
):
    formatter = ConsoleFormatter()

    formatter.display(
        make_prediction(
            accepted=True,
        )
    )

    output = capsys.readouterr().out

    assert "Prediction accepted" in output
    assert "75" in output


def test_displays_prediction_rejected(
    capsys,
):
    formatter = ConsoleFormatter()

    formatter.display(
        make_prediction(
            accepted=False,
        )
    )

    output = capsys.readouterr().out

    assert "Prediction rejected" in output
    assert "75" in output
