import pytest
from datetime import datetime, timedelta

from issuescout.scanner.relation.metadata_similarity import (
    MetadataSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_same_author_and_recent_pr():

    analyzer = MetadataSimilarityAnalyzer()

    created = datetime.now()

    issue = make_issue(
        author="alice",
        created_at=created,
    )

    pr = make_pull_request(
        author="alice",
        created_at=created + timedelta(days=2),
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence > 0


@pytest.mark.anyio
async def test_same_author_only():

    analyzer = MetadataSimilarityAnalyzer()

    issue = make_issue(
        author="alice",
    )

    pr = make_pull_request(
        author="alice",
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 5
    assert result.confidence == 30


@pytest.mark.anyio
async def test_no_metadata_match():

    analyzer = MetadataSimilarityAnalyzer()

    created = datetime.now()

    issue = make_issue(
        author="alice",
        created_at=created,
    )

    pr = make_pull_request(
        author="bob",
        created_at=created - timedelta(days=1),
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
