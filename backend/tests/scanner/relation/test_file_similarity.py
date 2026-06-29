import pytest

from issuescout.scanner.relation.file_similarity import (
    FileSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_matching_files():

    analyzer = FileSimilarityAnalyzer()

    issue = make_issue(
        mentioned_files={
            "Lib/test/test_json.py",
        },
    )

    pr = make_pull_request(
        changed_files={
            "Lib/test/test_json.py",
            "README.md",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence > 0


@pytest.mark.anyio
async def test_multiple_matching_files():

    analyzer = FileSimilarityAnalyzer()

    issue = make_issue(
        mentioned_files={
            "a.py",
            "b.py",
        },
    )

    pr = make_pull_request(
        changed_files={
            "b.py",
            "c.py",
            "a.py",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 67


@pytest.mark.anyio
async def test_no_matching_files():

    analyzer = FileSimilarityAnalyzer()

    issue = make_issue(
        mentioned_files={
            "a.py",
        },
    )

    pr = make_pull_request(
        changed_files={
            "b.py",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
