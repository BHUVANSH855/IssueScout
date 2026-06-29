from issuescout.scanner.relation.registry import (
    default_analyzers,
)


def test_returns_list():

    analyzers = default_analyzers()

    assert isinstance(
        analyzers,
        list,
    )


def test_expected_number_of_analyzers():

    analyzers = default_analyzers()

    assert len(analyzers) == 13


def test_analyzer_names_are_unique():

    analyzers = default_analyzers()

    names = [analyzer.metadata.name for analyzer in analyzers]

    assert len(names) == len(set(names))


def test_pipeline_order():

    analyzers = default_analyzers()

    names = [analyzer.metadata.name for analyzer in analyzers]

    assert names == [
        "timeline_reference",
        "commit_reference",
        "comment_reference",
        "body_reference",
        "commit_message_reference",
        "branch_similarity",
        "title_similarity",
        "commit_history_similarity",
        "label_similarity",
        "author_similarity",
        "metadata_similarity",
        "file_similarity",
        "reviewer_similarity",
    ]


def test_every_analyzer_enabled():

    analyzers = default_analyzers()

    assert all(analyzer.metadata.enabled for analyzer in analyzers)
