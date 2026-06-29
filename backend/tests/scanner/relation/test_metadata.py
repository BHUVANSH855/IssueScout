from issuescout.scanner.relation.metadata import (
    AnalyzerMetadata,
)


def test_create_metadata():

    metadata = AnalyzerMetadata(
        name="title",
        weight=25,
    )

    assert metadata.name == "title"
    assert metadata.weight == 25


def test_enabled_defaults_true():

    metadata = AnalyzerMetadata(
        name="title",
        weight=10,
    )

    assert metadata.enabled is True


def test_description_defaults_empty():

    metadata = AnalyzerMetadata(
        name="title",
        weight=10,
    )

    assert metadata.description == ""


def test_custom_values():

    metadata = AnalyzerMetadata(
        name="body",
        weight=40,
        enabled=False,
        description="Body analyzer",
    )

    assert metadata.enabled is False
    assert metadata.description == "Body analyzer"
