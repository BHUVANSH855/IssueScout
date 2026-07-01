from __future__ import annotations

import json
from pathlib import Path

from issuescout.evaluation.benchmark.suite import BenchmarkSuite


class BenchmarkWriter:
    """
    Writes benchmark suites to disk.

    The writer is intentionally independent of benchmark execution.
    It is responsible only for persisting completed benchmark results.

    Future versions may support additional formats such as CSV,
    Markdown, and HTML.
    """

    def write_json(
        self,
        suite: BenchmarkSuite,
        output_file: str | Path,
    ) -> None:
        """
        Serialize a benchmark suite to a JSON file.
        """

        output_path = Path(output_file)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "repositories": [
                {
                    "repository": benchmark.full_name,
                    "issue_count": benchmark.summary.issue_count,
                    "accuracy": benchmark.summary.accuracy,
                    "precision": benchmark.summary.precision,
                    "recall": benchmark.summary.recall,
                    "mrr": benchmark.summary.mrr,
                    "map": benchmark.summary.map,
                }
                for benchmark in suite.benchmarks
            ]
        }

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )
