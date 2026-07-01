from __future__ import annotations

from issuescout.evaluation.benchmark import (
    BenchmarkSuite,
    DEFAULT_BENCHMARK,
)


def benchmark() -> BenchmarkSuite:
    """
    Return the default benchmark suite.

    Future CLI options may allow selecting custom benchmark suites.
    """

    return DEFAULT_BENCHMARK
