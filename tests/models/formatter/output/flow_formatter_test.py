import pytest
from src.constants import GROUP_ID, TOPIC_ID
from src.model.formatter.output.flow_formatter import FlowOutputFormatter


class TestOutputFlowFormatter:
    @pytest.fixture
    def flow_output_formatter(self):
        return FlowOutputFormatter()

    @pytest.mark.formatter
    def test_initialization(self, flow_output_formatter):
        """Test that a FlowOutputFormatter instance can be created."""
        assert isinstance(flow_output_formatter, FlowOutputFormatter)

    @pytest.mark.formatter
    def test_is_group_or_topic(self, flow_output_formatter):
        """Test _is_group_or_topic method."""
        assert flow_output_formatter._is_group_or_topic(GROUP_ID + "_1", GROUP_ID)
        assert not flow_output_formatter._is_group_or_topic(TOPIC_ID + "_1", GROUP_ID)
        assert flow_output_formatter._is_group_or_topic(TOPIC_ID + "_1", TOPIC_ID)
        assert not flow_output_formatter._is_group_or_topic(GROUP_ID + "_1", TOPIC_ID)

    @pytest.mark.formatter
    def test_topic_is_assigned(self, flow_output_formatter):
        """Test _topic_is_assigned method."""
        assert flow_output_formatter._topic_is_assigned(1)
        assert not flow_output_formatter._topic_is_assigned(0)
        assert not flow_output_formatter._topic_is_assigned(2)

    @pytest.mark.formatter
    def test_get_groups_topics(self, flow_output_formatter):
        """Test _get_groups_topics method."""
        result = {
            GROUP_ID + "_1": {TOPIC_ID + "_1": 1, TOPIC_ID + "_2": 0},
            GROUP_ID + "_2": {TOPIC_ID + "_1": 0, TOPIC_ID + "_2": 1},
        }
        expected_result = {
            GROUP_ID + "_1": TOPIC_ID + "_1",
            GROUP_ID + "_2": TOPIC_ID + "_2",
        }
        assert flow_output_formatter._get_groups_topics(result) == expected_result

    @pytest.mark.formatter
    def test_tutor_is_assigned(self, flow_output_formatter):
        """Test _tutor_is_assigned method."""
        assert flow_output_formatter._tutor_is_assigned(1)
        assert not flow_output_formatter._tutor_is_assigned(0)
        assert flow_output_formatter._tutor_is_assigned(2)

    @pytest.mark.formatter
    def test_get_topics_tutors(self, flow_output_formatter):
        """Test _get_topics_tutors method."""
        result = {
            TOPIC_ID + "_1": {"tutor1": 1, "tutor2": 0},
            TOPIC_ID + "_2": {"tutor1": 0, "tutor2": 2},
        }
        expected_result = {TOPIC_ID + "_1": "tutor1", TOPIC_ID + "_2": "tutor2"}
        assert flow_output_formatter._get_topics_tutors(result) == expected_result
