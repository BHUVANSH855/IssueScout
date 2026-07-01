from __future__ import annotations

from issuescout.evaluation.dataset.builder import DatasetBuilder


def dataset(
    repository_owner: str,
    repository_name: str,
) -> DatasetBuilder:
    """
    Create a dataset builder for a repository.

    Parameters
    ----------
    repository_owner:
        GitHub repository owner.

    repository_name:
        GitHub repository name.
    """

    return DatasetBuilder(
        repository_owner=repository_owner,
        repository_name=repository_name,
    )
