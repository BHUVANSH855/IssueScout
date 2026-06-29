from issuescout.models.analysis import RelationPrediction


class Ranker:
    def rank(
        self,
        predictions: list[RelationPrediction],
    ) -> list[RelationPrediction]:

        return sorted(
            predictions,
            key=lambda prediction: prediction.score,
            reverse=True,
        )

    def best(
        self,
        predictions: list[RelationPrediction],
    ) -> RelationPrediction | None:

        ranked = self.rank(predictions)

        if not ranked:
            return None

        return ranked[0]
