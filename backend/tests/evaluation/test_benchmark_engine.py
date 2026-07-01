from issuescout.evaluation.benchmark.engine import BenchmarkEngine
from issuescout.evaluation.benchmark.repository import RepositoryBenchmark
from issuescout.evaluation.metrics.summary import EvaluationSummary


def test_benchmark_engine_builds_suite():

    engine = BenchmarkEngine()

    summary = EvaluationSummary(
        issue_count=10,
        accuracy=90.0,
        precision=88.0,
        recall=92.0,
        mrr=89.0,
        map=87.0,
    )

    benchmark = RepositoryBenchmark(
        repository_owner="python",
        repository_name="cpython",
        summary=summary,
    )

    suite = engine.run(
        [
            benchmark,
        ]
    )

    assert len(suite) == 1

    assert suite.benchmarks[0].full_name == "python/cpython"

    assert suite.benchmarks[0].summary.accuracy == 90.0


def test_benchmark_engine_empty_suite():

    engine = BenchmarkEngine()

    suite = engine.run([])

    assert len(suite) == 0

    assert suite.benchmarks == []
