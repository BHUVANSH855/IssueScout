from __future__ import annotations

import json
from pathlib import Path

from issuescout.evaluation.models import (
    EvaluationRecord,
    PredictionCandidate,
    RepositoryEvaluation,
)


class EvaluationLoader:
    """
    Loads evaluation datasets from JSON files.
    """

    def load(
        self,
        path: str | Path,
    ) -> RepositoryEvaluation:

        path = Path(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        records = []

        for record in data.get(
            "records",
            [],
        ):
            predictions = [
                PredictionCandidate(
                    pull_request_number=prediction["pull_request_number"],
                    score=prediction["score"],
                    confidence=prediction["confidence"],
                    rank=prediction["rank"],
                    matched=prediction.get(
                        "matched",
                        False,
                    ),
                )
                for prediction in record.get(
                    "predictions",
                    [],
                )
            ]

            records.append(
                EvaluationRecord(
                    repository=data["repository"],
                    issue_number=record["issue_number"],
                    actual_pull_request=record.get(
                        "actual_pull_request",
                    ),
                    predictions=predictions,
                )
            )

        return RepositoryEvaluation(
            repository=data["repository"],
            records=records,
        )
