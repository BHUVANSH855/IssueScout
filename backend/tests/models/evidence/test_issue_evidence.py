from issuescout.models.evidence.issue_evidence import (
    IssueEvidence,
)


def test_default_values():
    evidence = IssueEvidence()

    assert evidence.timeline_pull_requests == set()
    assert evidence.comment_pull_requests == set()
    assert evidence.commit_pull_requests == set()
    assert evidence.body_pull_requests == set()


def test_custom_values():
    evidence = IssueEvidence(
        timeline_pull_requests={1, 2},
        comment_pull_requests={3},
        commit_pull_requests={4, 5},
        body_pull_requests={6},
    )

    assert evidence.timeline_pull_requests == {1, 2}
    assert evidence.comment_pull_requests == {3}
    assert evidence.commit_pull_requests == {4, 5}
    assert evidence.body_pull_requests == {6}


def test_default_sets_are_independent():
    first = IssueEvidence()
    second = IssueEvidence()

    first.timeline_pull_requests.add(1)
    first.comment_pull_requests.add(2)
    first.commit_pull_requests.add(3)
    first.body_pull_requests.add(4)

    assert second.timeline_pull_requests == set()
    assert second.comment_pull_requests == set()
    assert second.commit_pull_requests == set()
    assert second.body_pull_requests == set()


def test_model_dump():
    evidence = IssueEvidence(
        timeline_pull_requests={1},
        comment_pull_requests={2},
        commit_pull_requests={3},
        body_pull_requests={4},
    )

    data = evidence.model_dump()

    assert data == {
        "timeline_pull_requests": {1},
        "comment_pull_requests": {2},
        "commit_pull_requests": {3},
        "body_pull_requests": {4},
    }
