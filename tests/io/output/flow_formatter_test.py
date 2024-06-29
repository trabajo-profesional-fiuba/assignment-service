import pytest
from src.io.output.flow_formatter import FlowOutputFormatter
from src.io.output.result_context import ResultContext
from src.exceptions import WrongDateFormat
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator
from src.model.group.group import Group


class TestFlowOutputFormatter:
    """
    Test cases for the `FlowOutputFormatter` class.
    """

    def create_groups(self, number, dates):
        groups = []
        for i in range(1, (number + 1)):
            g = Group(i)
            g.add_available_dates(dates)
            groups.append(g)

        return groups

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
        dates = [DeliveryDate(2, 2, 10), DeliveryDate(2, 2, 11)]
        groups = self.create_groups(2, dates)

        result_context = ResultContext(
            type="flow", groups=groups, result=flow_solver_result
        )

        result = formatter.get_result(result_context)
        assert "2-2-10" == groups[0].assigned_date.label()
        assert "2-2-11" == groups[1].assigned_date.label()

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
        substitutes = {"group-1": [evaluators[1]], "group-2": [evaluators[0]]}
        formatter = FlowOutputFormatter()
        dates_labels = [DeliveryDate(2, 2, 10).label(), DeliveryDate(2, 2, 11).label()]
        dates = [DeliveryDate(2, 2, 10), DeliveryDate(2, 2, 11)]
        groups = self.create_groups(2, dates)
        result_context = ResultContext(
            type="flow",
            groups=groups,
            evaluators=evaluators,
            evaluators_data=clean_results,
            result=flow_solver_result,
            substitutes=substitutes,
        )

        result = formatter.get_result(result_context)
        assert all(d.label() in dates_labels for d in evaluators[0].assigned_dates)
        assert all(d.label() in dates_labels for d in evaluators[1].assigned_dates)
