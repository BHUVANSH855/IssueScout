from unittest.mock import AsyncMock

import pytest

from issuescout.scanner.fetcher import Fetcher


@pytest.mark.anyio
async def test_close_closes_all_services():

    fetcher = Fetcher()

    fetcher.issue_service.close = AsyncMock()
    fetcher.repository_service.close = AsyncMock()
    fetcher.pull_request_service.close = AsyncMock()
    fetcher.review_service.close = AsyncMock()
    fetcher.commit_history_service.close = AsyncMock()

    await fetcher.close()

    fetcher.issue_service.close.assert_awaited_once()
    fetcher.repository_service.close.assert_awaited_once()
    fetcher.pull_request_service.close.assert_awaited_once()
    fetcher.review_service.close.assert_awaited_once()
    fetcher.commit_history_service.close.assert_awaited_once()


@pytest.mark.anyio
async def test_close_can_be_called_multiple_times():

    fetcher = Fetcher()

    fetcher.issue_service.close = AsyncMock()
    fetcher.repository_service.close = AsyncMock()
    fetcher.pull_request_service.close = AsyncMock()
    fetcher.review_service.close = AsyncMock()
    fetcher.commit_history_service.close = AsyncMock()

    await fetcher.close()
    await fetcher.close()

    assert fetcher.issue_service.close.await_count == 2
    assert fetcher.repository_service.close.await_count == 2
    assert fetcher.pull_request_service.close.await_count == 2
    assert fetcher.review_service.close.await_count == 2
    assert fetcher.commit_history_service.close.await_count == 2
