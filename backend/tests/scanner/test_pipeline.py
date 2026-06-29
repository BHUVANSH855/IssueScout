import pytest

from issuescout.models import (
    AnalysisResult,
    Repository,
    RepositoryScanContext,
)

from issuescout.scanner.pipeline import (
    AnalysisPipeline,
)

from tests.helpers.factories import (
    make_issue,
)


class FakeAnalyzer:
    def __init__(
        self,
        name: str,
        score: int,
    ):
        self.name = name
        self.score = score

        self.calls = []

    async def analyze(
        self,
        context,
        issue,
    ):

        self.calls.append(
            (
                context,
                issue,
            )
        )

        return AnalysisResult(
            analyzer=self.name,
            passed=True,
            score=self.score,
            reason=self.name,
        )


def make_context():

    return RepositoryScanContext(
        repository=Repository(
            owner="python",
            name="cpython",
        ),
    )


@pytest.mark.anyio
async def test_empty_pipeline():

    pipeline = AnalysisPipeline([])

    results = await pipeline.run(
        make_context(),
        make_issue(),
    )

    assert results == []


@pytest.mark.anyio
async def test_single_analyzer():

    analyzer = FakeAnalyzer(
        "assignment",
        20,
    )

    pipeline = AnalysisPipeline(
        [
            analyzer,
        ]
    )

    results = await pipeline.run(
        make_context(),
        make_issue(),
    )

    assert len(results) == 1
    assert results[0].analyzer == "assignment"
    assert results[0].score == 20


@pytest.mark.anyio
async def test_multiple_analyzers():

    first = FakeAnalyzer(
        "one",
        10,
    )

    second = FakeAnalyzer(
        "two",
        30,
    )

    pipeline = AnalysisPipeline(
        [
            first,
            second,
        ]
    )

    results = await pipeline.run(
        make_context(),
        make_issue(),
    )

    assert [result.analyzer for result in results] == [
        "one",
        "two",
    ]


@pytest.mark.anyio
async def test_execution_order():

    first = FakeAnalyzer(
        "first",
        1,
    )

    second = FakeAnalyzer(
        "second",
        2,
    )

    pipeline = AnalysisPipeline(
        [
            first,
            second,
        ]
    )

    await pipeline.run(
        make_context(),
        make_issue(),
    )

    assert len(first.calls) == 1
    assert len(second.calls) == 1


@pytest.mark.anyio
async def test_same_context_and_issue_are_passed():

    analyzer = FakeAnalyzer(
        "assignment",
        20,
    )

    pipeline = AnalysisPipeline(
        [
            analyzer,
        ]
    )

    context = make_context()
    issue = make_issue()

    await pipeline.run(
        context,
        issue,
    )

    called_context, called_issue = analyzer.calls[0]

    assert called_context is context
    assert called_issue is issue


@pytest.mark.anyio
async def test_results_are_returned_in_order():

    pipeline = AnalysisPipeline(
        [
            FakeAnalyzer(
                "a",
                1,
            ),
            FakeAnalyzer(
                "b",
                2,
            ),
            FakeAnalyzer(
                "c",
                3,
            ),
        ]
    )

    results = await pipeline.run(
        make_context(),
        make_issue(),
    )

    assert [result.score for result in results] == [
        1,
        2,
        3,
    ]
