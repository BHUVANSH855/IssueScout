import pytest

from issuescout.github.utils import Paginator


pytestmark = pytest.mark.anyio


async def test_fetch_all_single_page():
    paginator = Paginator()

    async def fetch(page: int):
        if page == 1:
            return [1, 2, 3]
        return []

    result = await paginator.fetch_all(fetch)

    assert result == [1, 2, 3]


async def test_fetch_all_multiple_pages():
    paginator = Paginator()

    pages = {
        1: [1, 2],
        2: [3, 4],
        3: [5],
    }

    async def fetch(page: int):
        return pages.get(page, [])

    result = await paginator.fetch_all(fetch)

    assert result == [1, 2, 3, 4, 5]


async def test_fetch_all_empty():
    paginator = Paginator()

    async def fetch(page: int):
        return []

    result = await paginator.fetch_all(fetch)

    assert result == []


async def test_fetch_all_stops_after_empty_page():
    paginator = Paginator()

    calls = []

    async def fetch(page: int):
        calls.append(page)

        if page == 1:
            return [1]

        return []

    result = await paginator.fetch_all(fetch)

    assert result == [1]
    assert calls == [1, 2]
