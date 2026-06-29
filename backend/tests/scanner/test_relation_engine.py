import pytest

from issuescout.scanner.relation.engine import (
    RelationEngine,
)
from issuescout.scanner.relation.factory import (
    create_relation_result,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


class StrongAnalyzer:
    async def analyze(
        self,
        issue,
        pull_request,
    ):
        return create_relation_result(
            analyzer="strong",
            score=40,
            confidence=100,
            reason="Strong evidence",
            evidence_type="strong",
        )


class SupportingAnalyzer:
    async def analyze(
        self,
        issue,
        pull_request,
    ):
        return create_relation_result(
            analyzer="supporting",
            score=20,
            confidence=80,
            reason="Supporting evidence",
        )


class ZeroAnalyzer:
    async def analyze(
        self,
        issue,
        pull_request,
    ):
        return create_relation_result(
            analyzer="zero",
            score=0,
            confidence=0,
            reason="No evidence",
        )


@pytest.mark.anyio
async def test_engine_combines_scores():

    engine = RelationEngine(
        [
            StrongAnalyzer(),
            SupportingAnalyzer(),
        ]
    )

    issue = make_issue()
    pr = make_pull_request()

    score, results = await engine.analyze(
        issue,
        pr,
    )

    assert score == 60
    assert len(results) == 2


@pytest.mark.anyio
async def test_engine_sorts_results_by_score():

    engine = RelationEngine(
        [
            SupportingAnalyzer(),
            StrongAnalyzer(),
            ZeroAnalyzer(),
        ]
    )

    issue = make_issue()
    pr = make_pull_request()

    score, results = await engine.analyze(
        issue,
        pr,
    )

    assert score == 60

    assert results[0].score == 40
    assert results[1].score == 20
    assert results[2].score == 0


@pytest.mark.anyio
async def test_confidence_levels():

    engine = RelationEngine([])

    assert engine.confidence_level(95) == "Very High"

    assert engine.confidence_level(75) == "High"

    assert engine.confidence_level(55) == "Medium"

    assert engine.confidence_level(35) == "Low"

    assert engine.confidence_level(10) == "Very Low"
