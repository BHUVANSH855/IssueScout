from __future__ import annotations

from issuescout.models import ScanResult
from issuescout.scanner.engine import ScannerEngine


class ApplicationScanService:
    """
    Application service for repository scanning.

    The service coordinates repository scans while leaving
    scan implementation to ScannerEngine.
    """

    def __init__(
        self,
        scanner: ScannerEngine,
    ) -> None:
        self._scanner = scanner

    async def scan_repository(
        self,
        owner: str,
        repository: str,
    ) -> ScanResult:
        return await self._scanner.scan_repository(
            owner,
            repository,
        )
