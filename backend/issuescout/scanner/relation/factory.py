from .result import RelationResult


def create_relation_result(
    *,
    analyzer: str,
    score: int,
    confidence: int,
    reason: str,
    evidence_type: str = "supporting",
    matched_issue_text: str | None = None,
    matched_pr_text: str | None = None,
    details: dict[str, str] | None = None,
) -> RelationResult:
    return RelationResult(
        analyzer=analyzer,
        score=score,
        confidence=confidence,
        reason=reason,
        evidence_type=evidence_type,
        matched_issue_text=matched_issue_text,
        matched_pr_text=matched_pr_text,
        details=details or {},
    )
