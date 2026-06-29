from unittest.mock import AsyncMock, Mock

import pytest

from issuescout.models import (
    AnalysisResult,
    Repository,
    RepositoryScanContext,
)
from issuescout.scanner.engine import ScannerEngine

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.fixture
def repository():
    return Repository(
        owner="python",
        name="cpython",
    )


@pytest.fixture
def passing_result():
    return AnalysisResult(
        analyzer="assignment",
        passed=True,
        score=100,
        reason="passed",
    )


@pytest.fixture
def failing_result():
    return AnalysisResult(
        analyzer="assignment",
        passed=False,
        score=0,
        reason="failed",
    )


@pytest.mark.anyio
async def test_scan_repository_returns_scan_result(
    repository,
    passing_result,
):
    issue = make_issue(
        number=123,
        title="Fix login bug",
        assigned=True,
        assignee="alice",
    )

    pr = make_pull_request(
        number=42,
        title="Fix login bug",
    )

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
        pull_requests=[pr],
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = pr

    pipeline = AsyncMock()
    pipeline.run.return_value = [
        passing_result,
    ]

    confidence = Mock()
    confidence.calculate.return_value = 95

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    result = await engine.scan_repository(
        "python",
        "cpython",
    )

    assert result.repository == "python/cpython"
    assert result.total_issues == 1
    assert result.available_issues == 1

    summary = result.issues[0]

    assert summary.number == 123
    assert summary.title == "Fix login bug"
    assert summary.assigned is True
    assert summary.assignee == "alice"
    assert summary.confidence == 95
    assert summary.linked_pr_number == 42
    assert summary.linked_pr_title == "Fix login bug"


@pytest.mark.anyio
async def test_scan_repository_filters_failed_issue(
    repository,
    failing_result,
):
    issue = make_issue()

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [
        failing_result,
    ]

    confidence = Mock()

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    result = await engine.scan_repository(
        "python",
        "cpython",
    )

    assert result.total_issues == 0
    assert result.available_issues == 0
    assert result.issues == []

    confidence.calculate.assert_not_called()

@pytest.mark.anyio
async def test_detector_called_for_each_issue(
    repository,
    passing_result,
):
    issues = [
        make_issue(number=1),
        make_issue(number=2),
        make_issue(number=3),
    ]

    context = RepositoryScanContext(
        repository=repository,
        issues=issues,
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 100

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    await engine.scan_repository(
        "python",
        "cpython",
    )

    assert detector.find_linked_pr.await_count == 3


@pytest.mark.anyio
async def test_pipeline_called_for_each_issue(
    repository,
    passing_result,
):
    issues = [
        make_issue(number=1),
        make_issue(number=2),
    ]

    context = RepositoryScanContext(
        repository=repository,
        issues=issues,
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 100

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    await engine.scan_repository(
        "python",
        "cpython",
    )

    assert pipeline.run.await_count == 2


@pytest.mark.anyio
async def test_confidence_calculated_for_each_accepted_issue(
    repository,
    passing_result,
):
    issues = [
        make_issue(number=1),
        make_issue(number=2),
    ]

    context = RepositoryScanContext(
        repository=repository,
        issues=issues,
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 87

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    await engine.scan_repository(
        "python",
        "cpython",
    )

    assert confidence.calculate.call_count == 2


@pytest.mark.anyio
async def test_scan_repository_handles_missing_linked_pr(
    repository,
    passing_result,
):
    issue = make_issue()

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 75

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    result = await engine.scan_repository(
        "python",
        "cpython",
    )

    summary = result.issues[0]

    assert summary.linked_pr_number is None
    assert summary.linked_pr_title is None

@pytest.mark.anyio
async def test_fetcher_closed_after_scan(
    repository,
    passing_result,
):
    issue = make_issue()

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 100

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    await engine.scan_repository(
        "python",
        "cpython",
    )

    fetcher.close.assert_awaited_once()


@pytest.mark.anyio
async def test_detector_closed_after_scan(
    repository,
    passing_result,
):
    issue = make_issue()

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
    )

    fetcher = AsyncMock()
    fetcher.fetch_context.return_value = context

    detector = AsyncMock()
    detector.find_linked_pr.return_value = None

    pipeline = AsyncMock()
    pipeline.run.return_value = [passing_result]

    confidence = Mock()
    confidence.calculate.return_value = 100

    engine = ScannerEngine(
        fetcher=fetcher,
        detector=detector,
        pipeline=pipeline,
        confidence=confidence,
    )

    await engine.scan_repository(
        "python",
        "cpython",
    )

    detector.close.assert_awaited_once()