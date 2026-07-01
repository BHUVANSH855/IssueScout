from issuescout.evaluation.benchmark.repository import RepositoryBenchmark
from issuescout.evaluation.benchmark.runner import BenchmarkRunner
from issuescout.evaluation.metrics.summary import EvaluationSummary


def test_runner_returns_suite():

    runner = BenchmarkRunner()

    summary = EvaluationSummary(
        issue_count=15,
        accuracy=82.5,
        precision=80.0,
        recall=81.0,
        mrr=84.0,
        map=79.5,
    )

    benchmark = RepositoryBenchmark(
        repository_owner="python",
        repository_name="cpython",
        summary=summary,
    )

    suite = runner.run(
        [
            benchmark,
        ]
    )

    assert len(suite) == 1

    assert suite.benchmarks[0].full_name == "python/cpython"

    assert suite.benchmarks[0].summary.accuracy == 82.5


def test_runner_handles_empty_input():

    runner = BenchmarkRunner()

    suite = runner.run([])

    assert len(suite) == 0

    assert suite.benchmarks == []
