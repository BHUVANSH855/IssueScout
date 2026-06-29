import json

from issuescout.models.analysis import PredictionResult


class JsonFormatter:
    """
    Formats prediction results as JSON.
    """

    def format(
        self,
        prediction: PredictionResult,
    ) -> dict:
        return prediction.model_dump()

    def dumps(
        self,
        prediction: PredictionResult,
        *,
        indent: int = 2,
    ) -> str:
        return json.dumps(
            self.format(prediction),
            indent=indent,
            ensure_ascii=False,
        )
