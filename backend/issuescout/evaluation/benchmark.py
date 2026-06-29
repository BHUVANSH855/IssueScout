from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class RepositoryBenchmark:
    """
    Represents a repository included in a benchmark.
    """

    owner: str
    repository: str
    issue_limit: int = 100


@dataclass(slots=True)
class BenchmarkSuite:
    """
    Collection of repositories used for benchmarking.
    """

    name: str
    repositories: list[RepositoryBenchmark] = field(default_factory=list)


DEFAULT_BENCHMARK = BenchmarkSuite(
    name="default",
    repositories=[
        RepositoryBenchmark(
            owner="python",
            repository="cpython",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="fastapi",
            repository="fastapi",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="pallets",
            repository="flask",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="pytest-dev",
            repository="pytest",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="psf",
            repository="requests",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="encode",
            repository="httpx",
            issue_limit=100,
        ),
        RepositoryBenchmark(
            owner="numpy",
            repository="numpy",
            issue_limit=100,
        ),
    ],
)
