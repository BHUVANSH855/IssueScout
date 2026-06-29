from urllib.parse import quote

from issuescout.core.logging import logger
from issuescout.github.client import GitHubClient


class PullRequestService:
    def __init__(self):
        self.client = GitHubClient()

    async def search_issue_references(
        self,
        owner: str,
        repo: str,
        issue_number: int,
    ):
        query = f'repo:{owner}/{repo} is:pr "{issue_number}"'

        logger.info(
            "Scanning issue #%s",
            issue_number,
        )

        logger.info(
            "Search query: %s",
            query,
        )

        endpoint = f"/search/issues?q={quote(query)}"

        logger.info(
            "Endpoint: %s",
            endpoint,
        )

        return await self.client.get(
            endpoint,
        )

    async def list_open_pull_requests(
        self,
        owner: str,
        repo: str,
    ):
        endpoint = f"/repos/{owner}/{repo}/pulls?state=open"

        logger.info(
            "Fetching open pull requests",
        )

        logger.info(
            "Endpoint: %s",
            endpoint,
        )

        return await self.client.get_all(
            endpoint,
        )

    async def get_pull_request_files(
        self,
        owner: str,
        repo: str,
        number: int,
    ):
        endpoint = f"/repos/{owner}/{repo}/pulls/{number}/files"

        return await self.client.get_all(
            endpoint,
        )

    async def get_pull_request_commits(
        self,
        owner: str,
        repo: str,
        number: int,
    ):
        endpoint = f"/repos/{owner}/{repo}/pulls/{number}/commits"

        return await self.client.get_all(
            endpoint,
        )

    async def close(self):
        await self.client.close()
