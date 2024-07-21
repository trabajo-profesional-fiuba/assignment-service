import pytest
from src.algorithms.adapters.exceptions import ResultFormatNotFound
from src.algorithms.adapters.result_adapter import ResultAdapter
from src.algorithms.adapters.flow_adapter import FlowAdapter
from src.algorithms.adapters.lp_adapter import LPAdapter
from src.algorithms.adapters.result_context import ResultContext
from src.model.utils.result import AssignmentResult


class TestResultAdapter:

    @pytest.mark.unit
    def test_initialization(self):
        formatter = ResultAdapter()
        assert formatter is not None

    @pytest.mark.unit
    def test_adapt_results_flow(self, mocker):
        formatter = ResultAdapter()
        context = ResultContext(type="flow")

        mocker.patch.object(
            FlowAdapter,
            "adapt_results",
            return_value=AssignmentResult([("group-1", "evaluator-1", "date-1-2-3")]),
        )

        formatted_result = formatter.adapt_results(context)
        assert isinstance(formatted_result, AssignmentResult)
        FlowAdapter.adapt_results.assert_called_once_with(context)

    @pytest.mark.unit
    def test_adapt_results_linear(self, mocker):
        formatter = ResultAdapter()
        context = ResultContext(type="linear")
        mocker.patch.object(
            LPAdapter,
            "adapt_results",
            return_value=AssignmentResult([("group-1", "evaluator-1", "date-1-2-3")]),
        )

        formatted_result = formatter.adapt_results(context)
        assert isinstance(formatted_result, AssignmentResult)
        LPAdapter.adapt_results.assert_called_once_with(context)

    @pytest.mark.unit
    def test_adapt_results_unrecognized_format(self):
        formatter = ResultAdapter()
        context = ResultContext(type="pepe")

        with pytest.raises(ResultFormatNotFound):
            formatter.adapt_results(context)

    @pytest.mark.unit
    def test_adapt_results_context_without_type_key(self):
        formatter = ResultAdapter()
        context = ResultContext(pepe="flow")

        with pytest.raises(ResultFormatNotFound):
            formatter.adapt_results(context)
