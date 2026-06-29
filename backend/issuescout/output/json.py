from issuescout.models.analysis import PredictionResult


class JsonFormatter:
    def format(
        self,
        prediction: PredictionResult,
    ) -> dict:

        return prediction.model_dump()
