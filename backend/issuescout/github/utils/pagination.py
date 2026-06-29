from collections.abc import Awaitable, Callable


class Paginator:
    """
    Helper for fetching paginated GitHub API results.
    """

    async def fetch_all(
        self,
        fetch_page: Callable[
            [int],
            Awaitable[list],
        ],
    ) -> list:
        page = 1
        results = []

        while True:
            items = await fetch_page(page)

            if not items:
                break

            results.extend(items)
            page += 1

        return results
