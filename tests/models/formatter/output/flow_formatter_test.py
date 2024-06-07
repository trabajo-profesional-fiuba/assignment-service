import pytest
from src.model.formatter.output.flow_formatter import FlowOutputFormatter
from src.exceptions import WrongDateFormat
from tests.algorithms.date_simplex.helper import TestLPHelper


class TestFlowOutputFormatter:
    formatter = FlowOutputFormatter()
    helper = TestLPHelper()

    @pytest.mark.unit
    def test_create_date_with_correct_format(self):
        assert "1-1-1" == self.formatter._create_date("date-1-1-1").label()

    @pytest.mark.unit
    def test_create_date_with_wrong_format(self):
        with pytest.raises(WrongDateFormat):
            assert "1-1-1" == self.formatter._create_date("1-1-1").label()

    @pytest.mark.unit
    def test_get_result_with_groups(self):
        flow_solver_result = {
            "s": {"group-1", "group-2"},
            "group-1": {"date-2-2-10": 1, "date-2-2-11": 0},
            "group-2": {"date-2-2-10": 0, "date-2-2-11": 1},
            "date-2-2-10": {"t": 1},
            "date-2-2-11": {"t": 1},
            "t": {},
        }

        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        result = self.formatter.get_result(flow_solver_result, groups, [])
        assert "2-2-10" == result.delivery_date_group(groups[0]).label()
        assert "2-2-11" == result.delivery_date_group(groups[1]).label()

    @pytest.mark.unit
    def test_get_result_with_evaluators(self):
        flow_solver_result = {
            "s": {"evaluator-1": 4, "evaluator-2": 4},
            "evaluator-1": {"date-1-evaluator-1": 2, "date-2-evaluator-1": 2},
            "evaluator-2": {"date-2-evaluator-2": 2, "date-3-evaluator-2": 2},
            "date-2-evaluator-1": {"date-2-2-10": 1, "date-2-2-11": 1},
            "date-2-2-10": {"t": 2},
            "date-2-2-11": {"t": 2},
            "date-2-evaluator-2": {"date-2-2-10": 1, "date-2-2-11": 1},
            "t": {},
        }

        num_evaluators = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        result = self.formatter.get_result(flow_solver_result, [], evaluators)
        assert result.delivery_date_evaluator(evaluators[0]) == []
        assert result.delivery_date_evaluator(evaluators[1]) == []

    @pytest.mark.unit
    def test_get_result_with_empty_result(self):
        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        result = self.formatter.get_result({}, groups, [])
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None

    @pytest.mark.unit
    def test_get_result_with_empty_groups(self):
        flow_solver_result = {
            "s": {"group-1", "group-2"},
            "group-1": {"date-2-2-10": 1, "date-2-2-11": 0},
            "group-2": {"date-2-2-10": 0, "date-2-2-11": 1},
            "date-2-2-10": {"t": 1},
            "date-2-2-11": {"t": 1},
            "t": {},
        }

        num_groups = 2
        num_evaluators = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        groups = self.helper.create_groups(num_groups, dates)

        result = self.formatter.get_result(flow_solver_result, [], evaluators)
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None
