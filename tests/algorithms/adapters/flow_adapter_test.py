import pytest

from src.algorithms.adapters.flow_adapter import FlowAdapter
from src.algorithms.adapters.result_context import ResultContext
from src.core.period import TutorPeriod
from src.core.group import Group
from src.exceptions import WrongDateFormat
from src.core.delivery_date import DeliveryDate


class TestFlowAdapter:
    """
    Test cases for the `FlowAdapter` class.
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
        formatter = FlowAdapter()
        assert "1-1-1" == formatter._create_date("date-1-1-1").label()

    @pytest.mark.unit
    def test_create_date_with_wrong_format(self):
        """
        Tests if _create_date raises WrongDateFormat for incorrectly formatted date
        strings.
        """
        formatter = FlowAdapter()
        with pytest.raises(WrongDateFormat):
            assert "1-1-1" == formatter._create_date("1-1-1").label()

    @pytest.mark.unit
    def test_adapt_results(self, mocker):
        """
        Tests adapt_results method for assigning delivery dates to evaluators based
        on the flow solver result.
        """
        ev1 = TutorPeriod("1C2024")
        mocker.patch.object(ev1, "id", return_value=2)
        evaluators = [ev1]
        clean_results = {
            "group-1": (2, 2),
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

        formatter = FlowAdapter()
        dates = [DeliveryDate(2, 2, 10), DeliveryDate(2, 2, 11)]
        groups = self.create_groups(2, dates)
        expected = [
            ("group-1", "evaluator-2", "date-2-2-10"),
            ("group-2", "evaluator-2", "date-2-2-11"),
        ]

        result = formatter._adapt_groups_and_evaluators(
            groups, evaluators, flow_solver_result, clean_results
        )

        assert all(d in expected for d in result)

    @pytest.mark.unit
    def test_adapt_results_assign_dates(self, mocker):
        """
        Tests adapt_results method for assigning delivery dates to evaluators based
        on the flow solver result.
        """
        ev1 = TutorPeriod("1C2024")
        mocker.patch.object(ev1, "id", return_value=2)
        evaluators = [ev1]
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

        formatter = FlowAdapter()
        dates = [DeliveryDate(2, 2, 10), DeliveryDate(2, 2, 11)]
        dates_labels = [d.label() for d in dates]
        groups = self.create_groups(2, dates)
        result_context = ResultContext(
            type="flow",
            groups=groups,
            evaluators=evaluators,
            evaluators_results=clean_results,
            groups_results=flow_solver_result,
        )

        _ = formatter.adapt_results(result_context)
        assert all(d.label() in dates_labels for d in ev1.as_evaluator_dates)
        assert groups[0].assigned_date.label() == "2-2-10"
        assert groups[1].assigned_date.label() == "2-2-11"
