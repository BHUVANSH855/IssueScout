from issuescout.models import (
    PredictionResult,
    RelationPrediction,
)

from issuescout.presentation.console_reporter import (
    ConsoleReporter,
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
        confidence="High",
        evidence=relation.results,
    )


def test_reports_no_prediction(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        PredictionResult(
            issue_number=1,
        )
    )

    output = capsys.readouterr().out

    assert "No prediction." in output


def test_reports_candidate_ranking(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        make_prediction(),
    )

    output = capsys.readouterr().out

    assert "Candidate Ranking" in output
    assert "PR #42 -> 90" in output


def test_reports_prediction_details(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        make_prediction(),
    )

    output = capsys.readouterr().out

    assert "Best candidate: PR #42" in output
    assert "Score: 90" in output
    assert "Confidence: High" in output


def test_reports_prediction_accepted(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        make_prediction(
            accepted=True,
        )
    )

    output = capsys.readouterr().out

    assert "Prediction accepted" in output


def test_reports_prediction_rejected(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        make_prediction(
            accepted=False,
        )
    )

    output = capsys.readouterr().out

    assert "Prediction rejected" in output


def test_reports_evidence(
    capsys,
):
    reporter = ConsoleReporter()

    reporter.report(
        make_prediction(),
    )

    output = capsys.readouterr().out

    assert "Evidence:" in output
    assert "- Title matched" in output