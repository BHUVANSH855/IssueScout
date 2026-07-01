from unittest.mock import AsyncMock, patch

import pytest

from issuescout.evaluation.dataset.generator import DatasetGenerator


pytestmark = pytest.mark.anyio


async def test_generate_dataset():

    with (
        patch(
            "issuescout.evaluation.dataset.generator.IssueService",
        ) as MockIssueService,
        patch(
            "issuescout.evaluation.dataset.generator.GroundTruthCollector",
        ) as MockGroundTruthCollector,
        patch(
            "issuescout.evaluation.dataset.generator.RepositoryCollector",
        ) as MockRepositoryCollector,
    ):
        issue_service = MockIssueService.return_value
        ground_truth = MockGroundTruthCollector.return_value
        repository_collector = MockRepositoryCollector.return_value

        issue_service.list_closed_issues = AsyncMock(
            return_value=[
                {"number": 1},
                {"number": 2, "pull_request": {}},
            ]
        )

        ground_truth.collect = AsyncMock(
            return_value="record",
        )

        repository_collector.build_dataset.return_value = "dataset"

        generator = DatasetGenerator()

        result = await generator.generate(
            "python",
            "cpython",
        )

        assert result == "dataset"

        issue_service.list_closed_issues.assert_awaited_once_with(
            "python",
            "cpython",
            limit=100,
        )

        ground_truth.collect.assert_awaited_once_with(
            "python",
            "cpython",
            1,
        )

        repository_collector.build_dataset.assert_called_once_with(
            ["record"],
        )


async def test_close():

    with (
        patch(
            "issuescout.evaluation.dataset.generator.IssueService",
        ) as MockIssueService,
        patch(
            "issuescout.evaluation.dataset.generator.GroundTruthCollector",
        ) as MockGroundTruthCollector,
    ):
        issue_service = MockIssueService.return_value
        ground_truth = MockGroundTruthCollector.return_value

        issue_service.close = AsyncMock()
        ground_truth.close = AsyncMock()

        generator = DatasetGenerator()

        await generator.close()

        issue_service.close.assert_awaited_once()
        ground_truth.close.assert_awaited_once()
