from __future__ import annotations

from issuescout.application.scan_service import (
    ApplicationScanService,
)
from issuescout.models import ScanResult


class ScanRepositoryUseCase:
    """
    Executes a repository scan.

    This use case coordinates repository scanning through the
    application layer.
    """

    def __init__(
        self,
        service: ApplicationScanService,
    ) -> None:
        self._service = service

    async def execute(
        self,
        owner: str,
        repository: str,
    ) -> ScanResult:
        return await self._service.scan_repository(
            owner,
            repository,
        )
