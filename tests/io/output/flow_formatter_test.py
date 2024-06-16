import pytest
from src.io.output.flow_formatter import FlowOutputFormatter
from src.io.output.result_context import ResultContext
from src.exceptions import WrongDateFormat
from tests.assignments.date.helper import TestLPHelper
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator


class TestFlowOutputFormatter:
    """
    Test cases for the `FlowOutputFormatter` class.
    """
    helper = TestLPHelper()

    @pytest.mark.unit
    def test_create_date_with_correct_format(self):
        """
        Tests if _create_date correctly parses a properly formatted date string.
        """
        formatter = FlowOutputFormatter()
        assert "1-1-1" == formatter._create_date("date-1-1-1").label()

    @pytest.mark.unit
    def test_create_date_with_wrong_format(self):
        """
        Tests if _create_date raises WrongDateFormat for incorrectly formatted date
        strings.
        """
        formatter = FlowOutputFormatter()
        with pytest.raises(WrongDateFormat):
            assert "1-1-1" == formatter._create_date("1-1-1").label()

    @pytest.mark.unit
    def test_get_result_with_groups(self):
        """
        Tests get_result method for assigning delivery dates to groups based on the flow
        solver result.
        """
        flow_solver_result = {
            "s": {"group-1", "group-2"},
            "group-1": {"date-2-2-10": 1, "date-2-2-11": 0},
            "group-2": {"date-2-2-10": 0, "date-2-2-11": 1},
            "date-2-2-10": {"t": 1},
            "date-2-2-11": {"t": 1},
            "t": {},
        }
        formatter = FlowOutputFormatter()
        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        result_context = ResultContext(
            type='flow', groups=groups, result=flow_solver_result)

        result = formatter.get_result(result_context)
        assert "2-2-10" == result.delivery_date_group(groups[0]).label()
        assert "2-2-11" == result.delivery_date_group(groups[1]).label()

    @pytest.mark.unit
    def test_get_result_with_evaluators(self):
        """
        Tests get_result method for assigning delivery dates to evaluators based on the
        flow solver result.
        """
        clean_results = {
            "group-1": (1, 2),
            "group-2": (2, 2),
        }

        flow_solver_result = {
            "s": {"group-1", "group-2"},
            "group-1": {"date-2-2-10": 1, "date-2-2-11": 0},
            "group-2": {"date-2-2-10": 0, "date-2-2-11": 1},
            "date-2-2-10": {"t": 1},
            "date-2-2-11": {"t": 1},
            "t": {},
        }
        formatter = FlowOutputFormatter()
        evaluators = [Evaluator(1), Evaluator(2)]
        dates = [DeliveryDate(2, 2, 10), DeliveryDate(2, 2, 11)]
        result_context = ResultContext(
            type='flow', evaluators=evaluators, evaluators_data=clean_results, result=flow_solver_result)

        result = formatter.get_result(result_context)
        assert result.delivery_date_evaluator(
            evaluators[0])[0].label() == dates[0].label()
        assert result.delivery_date_evaluator(
            evaluators[1])[0].label() == dates[1].label()

    @pytest.mark.unit
    def test_get_result_with_substitutes(self):
        """
        Tests get_result method for assigning delivery dates to evaluators based on the
        flow solver result.
        """
        evaluators = [Evaluator(1), Evaluator(2)]
        clean_results = {
            "group-1": (1, 2),
            "group-2": (2, 2),
        }
        flow_solver_result = {
            "s": {"group-1", "group-2"},
            "group-1": {"date-2-2-10": 1, "date-2-2-11": 0},
            "group-2": {"date-2-2-10": 0, "date-2-2-11": 1},
            "date-2-2-10": {"t": 1},
            "date-2-2-11": {"t": 1},
            "t": {},
        }
        substitutes = {
            "group-1": [evaluators[1]],
            "group-2": [evaluators[0]]
        }
        formatter = FlowOutputFormatter()
        dates = [DeliveryDate(2, 2, 10).label(), DeliveryDate(2, 2, 11).label()]
        result_context = ResultContext(type='flow', evaluators=evaluators,
                                       evaluators_data=clean_results, result=flow_solver_result, substitutes=substitutes)

        result = formatter.get_result(result_context)
        assert all(d.label() in dates for d in evaluators[0].assigned_dates)
        assert all(d.label() in dates for d in evaluators[1].assigned_dates)
