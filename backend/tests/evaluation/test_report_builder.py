from issuescout.evaluation.comparison.result import ComparisonResult
from issuescout.evaluation.metrics.summary import EvaluationSummary
from issuescout.evaluation.report_builder import ReportBuilder


def test_report_builder_builds_report():

    builder = ReportBuilder()

    comparison = ComparisonResult(
        repository_owner="python",
        repository_name="cpython",
        issue_number=123,
        actual_pull_request=456,
        predicted_pull_request=456,
        matched=True,
        rank=1,
        prediction_count=1,
        confidence=100.0,
    )

    summary = EvaluationSummary(
        issue_count=1,
        accuracy=100.0,
        precision=100.0,
        recall=100.0,
        mrr=100.0,
        map=100.0,
    )

    report = builder.build(
        repository="python/cpython",
        summary=summary,
        comparisons=[comparison],
    )

    assert report.repository == "python/cpython"
    assert report.metrics.total_issues == 1
    assert report.metrics.evaluated_issues == 1
    assert report.metrics.top1_accuracy == 100.0
    assert report.failures == []


def test_report_builder_collects_failures():

    builder = ReportBuilder()

    comparison = ComparisonResult(
        repository_owner="python",
        repository_name="cpython",
        issue_number=123,
        actual_pull_request=456,
        predicted_pull_request=None,
        matched=False,
        rank=None,
        prediction_count=5,
        confidence=0.0,
    )

    summary = EvaluationSummary(
        issue_count=1,
        accuracy=0.0,
        precision=0.0,
        recall=0.0,
        mrr=0.0,
        map=0.0,
    )

    report = builder.build(
        repository="python/cpython",
        summary=summary,
        comparisons=[comparison],
    )

    assert report.repository == "python/cpython"
    assert report.metrics.total_issues == 1
    assert report.metrics.evaluated_issues == 1
    assert report.metrics.top1_accuracy == 0.0

    assert len(report.failures) == 1

    failure = report.failures[0]

    assert failure.issue_number == 123
    assert failure.actual_pull_request == 456
    assert failure.predicted_pull_request is None
    assert failure.predicted_rank is None
    assert failure.prediction_score == 0.0
    assert failure.reason == "Prediction did not match ground truth."
