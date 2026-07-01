from __future__ import annotations

from issuescout.evaluation.dataset.generator import (
    DatasetGenerator,
)
from issuescout.evaluation.models import (
    RepositoryEvaluation,
)


class GenerateDatasetUseCase:
    """
    Generates an evaluation dataset for a repository.
    """

    def __init__(
        self,
        generator: DatasetGenerator | None = None,
    ) -> None:
        self._generator = generator or DatasetGenerator()

    async def execute(
        self,
        owner: str,
        repository: str,
        *,
        limit: int = 100,
    ) -> RepositoryEvaluation:
        return await self._generator.generate(
            owner,
            repository,
            limit=limit,
        )

    async def close(
        self,
    ) -> None:
        await self._generator.close()
