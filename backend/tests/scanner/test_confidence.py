from issuescout.models import (
    AnalysisResult,
)

from issuescout.scanner.confidence import (
    ConfidenceCalculator,
)


def make_result(
    score: int,
    passed: bool,
) -> AnalysisResult:

    return AnalysisResult(
        analyzer="test",
        passed=passed,
        score=score,
        reason="reason",
    )


def test_empty_results():

    calculator = ConfidenceCalculator()

    assert calculator.calculate([]) == 0


def test_single_passed_result():

    calculator = ConfidenceCalculator()

    results = [
        make_result(
            score=20,
            passed=True,
        ),
    ]

    assert calculator.calculate(results) == 20


def test_failed_results_are_ignored():

    calculator = ConfidenceCalculator()

    results = [
        make_result(
            score=20,
            passed=False,
        ),
        make_result(
            score=15,
            passed=False,
        ),
    ]

    assert calculator.calculate(results) == 0


def test_mixed_results():

    calculator = ConfidenceCalculator()

    results = [
        make_result(
            score=20,
            passed=True,
        ),
        make_result(
            score=15,
            passed=False,
        ),
        make_result(
            score=30,
            passed=True,
        ),
    ]

    assert calculator.calculate(results) == 50


def test_multiple_passed_results():

    calculator = ConfidenceCalculator()

    results = [
        make_result(
            score=10,
            passed=True,
        ),
        make_result(
            score=15,
            passed=True,
        ),
        make_result(
            score=25,
            passed=True,
        ),
    ]

    assert calculator.calculate(results) == 50
