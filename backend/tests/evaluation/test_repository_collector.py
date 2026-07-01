from issuescout.evaluation.collector.repository import RepositoryCollector
from issuescout.evaluation.models import (
    EvaluationRecord,
    GroundTruthRecord,
)


def test_repository_collector_properties():

    collector = RepositoryCollector(
        "python",
        "cpython",
    )

    assert collector.repository_owner == "python"
    assert collector.repository_name == "cpython"
    assert collector.repository == "python/cpython"


def test_build_dataset():

    collector = RepositoryCollector(
        "python",
        "cpython",
    )

    ground_truth = GroundTruthRecord(
        repository_owner="python",
        repository_name="cpython",
        issue_number=1,
        issue_title="Example issue",
        issue_state="closed",
        actual_pull_request=100,
    )

    evaluation = collector.build_dataset(
        [
            EvaluationRecord(
                ground_truth=ground_truth,
            )
        ]
    )

    assert evaluation.repository_owner == "python"
    assert evaluation.repository_name == "cpython"
    assert len(evaluation.records) == 1
