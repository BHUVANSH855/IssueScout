from __future__ import annotations

from issuescout.services.repository_service import RepositoryService


class ApplicationRepositoryService:
    """
    Application service for repository operations.

    Coordinates repository-related use cases while delegating
    GitHub communication to RepositoryService.
    """

    def __init__(
        self,
        service: RepositoryService | None = None,
    ) -> None:
        self._service = service or RepositoryService()

    async def get_repository(
        self,
        owner: str,
        repository: str,
    ) -> dict:
        return await self._service.get_repository(
            owner,
            repository,
        )

    async def close(self) -> None:
        await self._service.close()
