from __future__ import annotations

from issuescout.evaluation.benchmark.engine import BenchmarkEngine
from issuescout.evaluation.benchmark.repository import RepositoryBenchmark
from issuescout.evaluation.benchmark.suite import BenchmarkSuite


class BenchmarkRunner:
    """
    High-level entry point for benchmark execution.

    The runner coordinates benchmark execution while delegating
    suite construction to the BenchmarkEngine.

    Future implementations will collect repository data,
    execute IssueScout evaluations, and construct
    RepositoryBenchmark instances automatically.
    """

    def __init__(self) -> None:
        self._engine = BenchmarkEngine()

    def run(
        self,
        benchmarks: list[RepositoryBenchmark],
    ) -> BenchmarkSuite:
        """
        Execute a benchmark run.

        Currently this builds a benchmark suite from an
        existing collection of repository benchmark results.
        """

        return self._engine.run(
            benchmarks,
        )
