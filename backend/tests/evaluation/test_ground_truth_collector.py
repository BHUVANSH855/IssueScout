import pytest

from issuescout.evaluation.collector.collector import GroundTruthCollector


def test_ground_truth_collector_is_abstract():

    with pytest.raises(TypeError):
        GroundTruthCollector()
