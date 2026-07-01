from __future__ import annotations

from issuescout.evaluation.benchmark.repository import RepositoryBenchmark
from issuescout.evaluation.benchmark.suite import BenchmarkSuite


class BenchmarkEngine:
    """
    Coordinates benchmark execution across multiple repositories.

    The engine is intentionally lightweight. It builds a benchmark suite
    from completed repository benchmark results. Future versions will be
    responsible for collecting datasets, executing evaluations, and
    producing RepositoryBenchmark objects automatically.
    """

    def run(
        self,
        benchmarks: list[RepositoryBenchmark],
    ) -> BenchmarkSuite:
        """
        Build a benchmark suite from repository benchmark results.
        """

        suite = BenchmarkSuite()

        for benchmark in benchmarks:
            suite.add(
                benchmark,
            )

        return suite
