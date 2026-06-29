from __future__ import annotations

from http import HTTPStatus

import httpx

from issuescout.core.config import settings
from issuescout.core.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)
from issuescout.core.logging import logger


class GitHubClient:
    """Asynchronous GitHub REST API client."""

    def __init__(self) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "IssueScout",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        self.client = httpx.AsyncClient(
            base_url=settings.GITHUB_API,
            headers=headers,
            timeout=30.0,
        )

    async def get(
        self,
        endpoint: str,
        headers: dict | None = None,
    ):
        logger.info(
            "GET %s",
            endpoint,
        )

        response = await self.client.get(
            endpoint,
            headers=headers,
        )

        if response.status_code >= HTTPStatus.BAD_REQUEST:
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

        return response.json()

    async def close(self):
        await self.client.aclose()
