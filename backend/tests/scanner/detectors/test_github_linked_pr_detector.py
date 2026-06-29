from unittest.mock import AsyncMock, Mock

import pytest

from issuescout.models import (
    PredictionResult,
    RelationPrediction,
    Repository,
    RepositoryScanContext,
)
from issuescout.scanner.detectors import GitHubLinkedPRDetector
from issuescout.scanner.relation.result import RelationResult

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
def relation_result():
    return RelationResult(
        analyzer="title",
        score=100,
        confidence=100,
        reason="Title matched",
    )


@pytest.mark.anyio
async def test_returns_predicted_pull_request(
    repository,
    relation_result,
):
    issue = make_issue(number=123)

    pull_request = make_pull_request(
        number=42,
        title="Fix login bug",
    )

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
        pull_requests=[pull_request],
    )

    prediction = PredictionResult(
        issue_number=123,
        prediction=RelationPrediction(
            pull_request=pull_request,
            score=100,
            results=[relation_result],
        ),
        accepted=True,
    )

    evidence = AsyncMock()

    prediction_service = AsyncMock()
    prediction_service.predict.return_value = prediction

    reporter = Mock()

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
        prediction_service=prediction_service,
        console_reporter=reporter,
    )

    result = await detector.find_linked_pr(
        context,
        123,
    )

    assert result == pull_request

    evidence.collect.assert_awaited_once_with(
        context,
        issue,
    )

    prediction_service.predict.assert_awaited_once_with(
        issue,
        context.pull_requests,
    )

    reporter.report.assert_called_once_with(
        prediction,
    )


@pytest.mark.anyio
async def test_returns_none_when_prediction_missing(
    repository,
):
    issue = make_issue(number=123)

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
        pull_requests=[],
    )

    prediction = PredictionResult(
        issue_number=123,
    )

    evidence = AsyncMock()

    prediction_service = AsyncMock()
    prediction_service.predict.return_value = prediction

    reporter = Mock()

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
        prediction_service=prediction_service,
        console_reporter=reporter,
    )

    result = await detector.find_linked_pr(
        context,
        123,
    )

    assert result is None

    evidence.collect.assert_awaited_once()

    prediction_service.predict.assert_awaited_once()

    reporter.report.assert_not_called()


@pytest.mark.anyio
async def test_close_delegates_to_evidence_collector():
    evidence = AsyncMock()

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
    )

    await detector.close()

    evidence.close.assert_awaited_once()


@pytest.mark.anyio
async def test_prediction_receives_repository_pull_requests(
    repository,
):
    issue = make_issue(number=123)

    pull_requests = [
        make_pull_request(number=1),
        make_pull_request(number=2),
    ]

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
        pull_requests=pull_requests,
    )

    prediction = PredictionResult(
        issue_number=123,
    )

    evidence = AsyncMock()

    prediction_service = AsyncMock()
    prediction_service.predict.return_value = prediction

    reporter = Mock()

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
        prediction_service=prediction_service,
        console_reporter=reporter,
    )

    await detector.find_linked_pr(
        context,
        123,
    )

    args = prediction_service.predict.await_args.args

    assert args[0] == issue
    assert args[1] == pull_requests


@pytest.mark.anyio
async def test_correct_issue_selected_from_context(
    repository,
):
    issue1 = make_issue(number=1)
    issue2 = make_issue(number=2)

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue1, issue2],
        pull_requests=[],
    )

    prediction = PredictionResult(
        issue_number=2,
    )

    evidence = AsyncMock()

    prediction_service = AsyncMock()
    prediction_service.predict.return_value = prediction

    reporter = Mock()

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
        prediction_service=prediction_service,
        console_reporter=reporter,
    )

    await detector.find_linked_pr(
        context,
        2,
    )

    args = prediction_service.predict.await_args.args

    assert args[0].number == 2


@pytest.mark.anyio
async def test_evidence_collected_before_prediction(
    repository,
):
    issue = make_issue()

    context = RepositoryScanContext(
        repository=repository,
        issues=[issue],
        pull_requests=[],
    )

    order = []

    evidence = AsyncMock()

    async def collect(*args, **kwargs):
        order.append("collect")

    evidence.collect.side_effect = collect

    prediction_service = AsyncMock()

    async def predict(*args, **kwargs):
        order.append("predict")
        return PredictionResult(
            issue_number=issue.number,
        )

    prediction_service.predict.side_effect = predict

    detector = GitHubLinkedPRDetector(
        evidence_collector=evidence,
        prediction_service=prediction_service,
        console_reporter=Mock(),
    )

    await detector.find_linked_pr(
        context,
        issue.number,
    )

    assert order == [
        "collect",
        "predict",
    ]
