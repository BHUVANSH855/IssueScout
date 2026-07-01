from __future__ import annotations

import csv
import json
from pathlib import Path

from issuescout.evaluation.models import RepositoryEvaluation


class EvaluationExporter:
    """
    Exports repository evaluation results to CSV and JSON.
    """

    def export_csv(
        self,
        evaluation: RepositoryEvaluation,
        output_file: str | Path,
    ) -> None:
        output_path = Path(output_file)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    "repository",
                    "issue_number",
                    "actual_pull_request",
                    "predicted_pull_request",
                    "rank",
                    "score",
                    "confidence",
                    "matched",
                ]
            )

            for record in evaluation.records:
                ground_truth = record.ground_truth

                for prediction in record.predictions:
                    writer.writerow(
                        [
                            evaluation.full_name,
                            ground_truth.issue_number,
                            ground_truth.actual_pull_request,
                            prediction.pull_request_number,
                            prediction.rank,
                            prediction.score,
                            prediction.confidence,
                            prediction.matched,
                        ]
                    )

    def export_json(
        self,
        evaluation: RepositoryEvaluation,
        output_file: str | Path,
    ) -> None:
        output_path = Path(output_file)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "repository": evaluation.full_name,
            "records": [],
        }

        for record in evaluation.records:
            ground_truth = record.ground_truth

            data["records"].append(
                {
                    "issue_number": ground_truth.issue_number,
                    "issue_title": ground_truth.issue_title,
                    "issue_state": ground_truth.issue_state,
                    "actual_pull_request": ground_truth.actual_pull_request,
                    "linkage_method": ground_truth.linkage_method,
                    "predictions": [
                        {
                            "pull_request_number": prediction.pull_request_number,
                            "rank": prediction.rank,
                            "score": prediction.score,
                            "confidence": prediction.confidence,
                            "matched": prediction.matched,
                        }
                        for prediction in record.predictions
                    ],
                }
            )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
            )
