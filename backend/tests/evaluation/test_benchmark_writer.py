import json

from issuescout.evaluation.benchmark.repository import RepositoryBenchmark
from issuescout.evaluation.benchmark.suite import BenchmarkSuite
from issuescout.evaluation.benchmark.writer import BenchmarkWriter
from issuescout.evaluation.metrics.summary import EvaluationSummary


def test_writer_exports_json(
    tmp_path,
):

    summary = EvaluationSummary(
        issue_count=25,
        accuracy=84.5,
        precision=82.0,
        recall=80.0,
        mrr=86.0,
        map=81.5,
    )

    benchmark = RepositoryBenchmark(
        repository_owner="python",
        repository_name="cpython",
        summary=summary,
    )

    suite = BenchmarkSuite()

    suite.add(
        benchmark,
    )

    output = tmp_path / "benchmark.json"

    BenchmarkWriter().write_json(
        suite,
        output,
    )

    assert output.exists()

    data = json.loads(
        output.read_text(
            encoding="utf-8",
        )
    )

    assert len(data["repositories"]) == 1

    repository = data["repositories"][0]

    assert repository["repository"] == "python/cpython"

    assert repository["accuracy"] == 84.5

    assert repository["issue_count"] == 25
