from __future__ import annotations

import asyncio
from http import HTTPStatus
from asyncio import Semaphore
import httpx

from issuescout.core.config import settings
from issuescout.core.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)
from issuescout.core.logging import logger
from issuescout.github.cache import GitHubCache


class GitHubClient:
    """Asynchronous GitHub REST API client with automatic retries."""

    _request_semaphore = Semaphore(
        settings.MAX_CONCURRENT_REQUESTS,
    )

    def __init__(self) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": settings.APP_NAME,
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        self.client = httpx.AsyncClient(
            base_url=settings.GITHUB_API,
            headers=headers,
            timeout=settings.REQUEST_TIMEOUT,
        )
        self.cache = GitHubCache()

    async def get(
        self,
        endpoint: str,
        headers: dict | None = None,
    ):
        cache_key = endpoint

        if headers:
            cache_key += str(sorted(headers.items()))

        cached = self.cache.get(cache_key)

        if cached is not None:
            logger.debug("Cache hit: %s", endpoint)
            return cached
        logger.info(
            "GET %s",
            endpoint,
        )

        retries = settings.GITHUB_MAX_RETRIES

        for attempt in range(retries + 1):
            try:
                async with self._request_semaphore:
                    response = await self.client.get(
                        endpoint,
                        headers=headers,
                    )

                break

            except (
                httpx.RemoteProtocolError,
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.NetworkError,
            ) as exc:
                if attempt >= retries:
                    raise GitHubAPIError(
                        f"GitHub request failed after {retries} retries."
                    ) from exc

                delay = settings.GITHUB_RETRY_BACKOFF * (2**attempt)

                logger.warning(
                    (
                        "Transient GitHub network error "
                        "(attempt %d/%d). "
                        "Retrying in %.1f seconds..."
                    ),
                    attempt + 1,
                    retries,
                    delay,
                )

                await asyncio.sleep(delay)

        if (
            response.status_code >= HTTPStatus.BAD_REQUEST
            and response.status_code != HTTPStatus.NOT_FOUND
        ):
            logger.error(
                "GitHub API returned %s",
                response.status_code,
            )
            logger.error(
                "%s",
                response.text,
            )

        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise GitHubAuthenticationError("GitHub authentication failed.")

        if response.status_code == HTTPStatus.FORBIDDEN:
            raise GitHubRateLimitError("GitHub API rate limit exceeded.")

        if response.status_code == HTTPStatus.NOT_FOUND:
            raise GitHubNotFoundError(f"GitHub resource not found: {endpoint}")

        if response.status_code >= HTTPStatus.BAD_REQUEST:
            raise GitHubAPIError(
                (f"GitHub API returned {response.status_code}: {response.text}")
            )

        data = response.json()

        self.cache.set(
            cache_key,
            data,
        )

        return data

    async def get_all(
        self,
        endpoint: str,
        *,
        page_size: int | None = None,
        headers: dict | None = None,
    ):
        """
        Retrieve every page from a GitHub REST endpoint.

        Works for endpoints returning JSON arrays.
        """

        page_size = page_size or settings.MAX_PAGE_SIZE

        page = 1

        results = []

        while True:
            separator = "&" if "?" in endpoint else "?"

            page_endpoint = f"{endpoint}{separator}per_page={page_size}&page={page}"

            data = await self.get(
                page_endpoint,
                headers=headers,
            )

            if not data:
                break

            results.extend(data)

            if len(data) < page_size:
                break

            page += 1

        return results

    async def close(self):
        await self.client.aclose()
