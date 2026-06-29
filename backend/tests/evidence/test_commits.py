import pytest

from issuescout.evidence.commits import (
    CommitEvidenceCollector,
)
from issuescout.models import Repository
from tests.helpers.factories import (
    make_issue,
)


@pytest.mark.anyio
async def test_collect_returns_none():

    collector = CommitEvidenceCollector()

    repository = Repository(
        owner="python",
        name="cpython",
    )

    issue = make_issue()

    result = await collector.collect(
        repository,
        issue,
    )

    assert result is None


@pytest.mark.anyio
async def test_collect_does_not_modify_issue():

    collector = CommitEvidenceCollector()

    repository = Repository(
        owner="python",
        name="cpython",
    )

    issue = make_issue()

    before = issue.model_copy(deep=True)

    await collector.collect(
        repository,
        issue,
    )

    assert issue == before
