from issuescout.models.issue import Issue
from issuescout.models.pull_request import PullRequest


def make_issue(**overrides) -> Issue:
    data = {
        "number": 123,
        "title": "Fix login bug",
        "author": "alice",
        "assignee": None,
        "assigned": False,
        "state": "open",
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "milestone": None,
        "labels": set(),
        "mentioned_files": set(),
        "timeline_pull_requests": set(),
        "comment_pull_requests": set(),
        "body_pull_requests": set(),
        "commit_pull_requests": set(),
    }

    data.update(overrides)
    return Issue(**data)


def make_pull_request(**overrides) -> PullRequest:
    data = {
        "number": 10,
        "title": "Fix login bug",
        "body": "",
        "author": "alice",
        "branch_name": "fix/login-bug",
        "state": "open",
        "draft": False,
        "created_at": None,
        "updated_at": None,
        "closed_at": None,
        "merged_at": None,
        "labels": set(),
        "reviewers": set(),
        "changed_files": set(),
        "commit_messages": [],
        "branch_commit_history": [],
        "related_issues": set(),
    }

    data.update(overrides)
    return PullRequest(**data)
