from __future__ import annotations

from issuescout.evaluation.dataset.builder import DatasetBuilder
from issuescout.evaluation.models import (
    GroundTruthRecord,
    RepositoryEvaluation,
)


class RepositoryCollector:
    """
    Collects and builds an evaluation dataset for a repository.

    At present this class assembles an existing collection of
    GroundTruthRecord objects into a RepositoryEvaluation.

    In future versions it will become responsible for collecting the
    records directly from GitHub through the GroundTruthCollector.
    """

    def __init__(
        self,
        repository_owner: str,
        repository_name: str,
    ) -> None:
        self.repository_owner = repository_owner
        self.repository_name = repository_name

    @property
    def repository(self) -> str:
        """
        Fully-qualified repository name.
        """
        return f"{self.repository_owner}/{self.repository_name}"

    def build_dataset(
        self,
        records: list[GroundTruthRecord],
    ) -> RepositoryEvaluation:
        """
        Build a repository evaluation dataset from ground-truth records.
        """
        builder = DatasetBuilder(
            repository_owner=self.repository_owner,
            repository_name=self.repository_name,
        )

        for record in records:
            builder.add_record(record)

        return builder.build()
