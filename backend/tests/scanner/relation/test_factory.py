from issuescout.scanner.relation.factory import (
    create_relation_result,
)


def test_create_minimal_result():

    result = create_relation_result(
        analyzer="title",
        score=10,
        confidence=50,
        reason="matched",
    )

    assert result.analyzer == "title"
    assert result.score == 10
    assert result.confidence == 50
    assert result.reason == "matched"
    assert result.evidence_type == "supporting"
    assert result.details == {}
    assert result.matched_issue_text is None
    assert result.matched_pr_text is None


def test_create_full_result():

    result = create_relation_result(
        analyzer="body",
        score=45,
        confidence=100,
        reason="exact",
        evidence_type="strong",
        matched_issue_text="issue",
        matched_pr_text="pr",
        details={
            "source": "body",
        },
    )

    assert result.analyzer == "body"
    assert result.score == 45
    assert result.confidence == 100
    assert result.evidence_type == "strong"
    assert result.matched_issue_text == "issue"
    assert result.matched_pr_text == "pr"
    assert result.details == {
        "source": "body",
    }


def test_none_details_becomes_empty_dict():

    result = create_relation_result(
        analyzer="x",
        score=1,
        confidence=1,
        reason="ok",
        details=None,
    )

    assert result.details == {}


def test_empty_details_preserved():

    result = create_relation_result(
        analyzer="x",
        score=1,
        confidence=1,
        reason="ok",
        details={},
    )

    assert result.details == {}
