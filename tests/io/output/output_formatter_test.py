import pytest
from src.io.output.output_formatter import OutputFormatter
from src.io.output.result_context import ResultContext
from src.io.output.flow_formatter import FlowOutputFormatter
from src.io.output.lp_formatter import LPOutputFormatter
from src.exceptions import ResultFormatNotFound
from src.model.group.group import Group
from src.model.utils.result import AssignmentResult
from src.model.utils.evaluator import Evaluator

class TestOutputFormatter:

    @pytest.mark.unit
    def test_initialization(self):
        formatter = OutputFormatter()
        assert formatter is not None

    @pytest.mark.unit
    def test_format_result_flow(self, mocker):
        formatter = OutputFormatter()
        context = ResultContext(type="flow")

        mocker.patch.object(
            FlowOutputFormatter,
            "get_result",
            return_value=AssignmentResult([], []),
        )

        formatted_result = formatter.format_result(context)
        assert isinstance(formatted_result, AssignmentResult)
        FlowOutputFormatter.get_result.assert_called_once_with(context)

    @pytest.mark.unit
    def test_format_result_linear(self, mocker):
        formatter = OutputFormatter()
        context = ResultContext(type="linear")
        mocker.patch.object(
            LPOutputFormatter,
            "get_result",
            return_value=AssignmentResult([], []),
        )

        formatted_result = formatter.format_result(context)
        assert isinstance(formatted_result, AssignmentResult)
        LPOutputFormatter.get_result.assert_called_once_with(context)

    @pytest.mark.unit
    def test_format_result_unrecognized_format(self):
        formatter = OutputFormatter()
        context = ResultContext(type="pepe")

        with pytest.raises(ResultFormatNotFound):
            formatter.format_result(context)

    @pytest.mark.unit
    def test_format_result_context_without_type_key(self):
        formatter = OutputFormatter()
        context = ResultContext(pepe="flow")

        with pytest.raises(ResultFormatNotFound):
            formatter.format_result(context)
