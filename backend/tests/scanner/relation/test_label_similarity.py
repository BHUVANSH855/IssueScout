import pytest

from issuescout.scanner.relation.label_similarity import (
    LabelSimilarityAnalyzer,
)

from tests.helpers.factories import (
    make_issue,
    make_pull_request,
)


@pytest.mark.anyio
async def test_identical_labels():

    analyzer = LabelSimilarityAnalyzer()

    issue = make_issue(
        labels={
            "bug",
            "docs",
        },
    )

    pr = make_pull_request(
        labels={
            "bug",
            "docs",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert result.confidence == 100


@pytest.mark.anyio
async def test_partial_label_overlap():

    analyzer = LabelSimilarityAnalyzer()

    issue = make_issue(
        labels={
            "bug",
            "performance",
        },
    )

    pr = make_pull_request(
        labels={
            "bug",
            "enhancement",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score > 0
    assert 0 < result.confidence < 100


@pytest.mark.anyio
async def test_no_common_labels():

    analyzer = LabelSimilarityAnalyzer()

    issue = make_issue(
        labels={
            "bug",
        },
    )

    pr = make_pull_request(
        labels={
            "documentation",
        },
    )

    result = await analyzer.analyze(
        issue,
        pr,
    )

    assert result.score == 0
    assert result.confidence == 0
