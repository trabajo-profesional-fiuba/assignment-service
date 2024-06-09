import pytest
from src.io.output.output_formatter import OutputFormatter
from src.io.output.flow_formatter import FlowOutputFormatter
from src.io.output.lp_formatter import LPOutputFormatter
from src.exceptions import ResultFormatNotFound
from src.model.group.group import Group
from src.model.utils.result import AssignmentResult
from src.model.utils.evaluator import Evaluator


class TestOutputFormatter:
    @pytest.fixture
    def setup_data(self):
        groups = [Group(1), Group(2)]
        evaluators = [Evaluator(1), Evaluator(2)]
        return groups, evaluators

    @pytest.mark.unit
    def test_initialization(self):
        formatter = OutputFormatter()
        assert formatter is not None

    @pytest.mark.unit
    def test_format_result_dict(self, mocker, setup_data):
        formatter = OutputFormatter()
        result = {"key": "value"}
        groups, evaluators = setup_data

        mocker.patch.object(
            FlowOutputFormatter,
            "get_result",
            return_value=AssignmentResult(groups, evaluators),
        )

        formatted_result = formatter.format_result(result, groups, evaluators)
        assert isinstance(formatted_result, AssignmentResult)
        FlowOutputFormatter.get_result.assert_called_once_with(
            result, groups, evaluators
        )

    @pytest.mark.unit
    def test_format_result_list(self, mocker, setup_data):
        formatter = OutputFormatter()
        result = ["item1", "item2"]
        groups, evaluators = setup_data

        mocker.patch.object(
            LPOutputFormatter,
            "get_result",
            return_value=AssignmentResult(groups, evaluators),
        )

        formatted_result = formatter.format_result(result, groups, evaluators)
        assert isinstance(formatted_result, AssignmentResult)
        LPOutputFormatter.get_result.assert_called_once_with(result, groups, evaluators)

    @pytest.mark.unit
    def test_format_result_unrecognized_format(self, setup_data):
        formatter = OutputFormatter()
        result = "unrecognized_format"
        groups, evaluators = setup_data

        with pytest.raises(ResultFormatNotFound):
            formatter.format_result(result, groups, evaluators)
