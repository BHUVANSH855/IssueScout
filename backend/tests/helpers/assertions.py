from issuescout.scanner.relation.result import RelationResult


def assert_positive(result: RelationResult):
    assert result.score > 0
    assert result.confidence > 0


def assert_negative(result: RelationResult):
    assert result.score == 0
    assert result.confidence == 0


def assert_strong(result: RelationResult):
    assert result.evidence_type == "strong"


def assert_supporting(result: RelationResult):
    assert result.evidence_type == "supporting"


def assert_reason_contains(
    result: RelationResult,
    text: str,
):
    assert text.lower() in result.reason.lower()
