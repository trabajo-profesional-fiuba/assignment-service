import pytest
from src.model.formatter.output.lp_formatter import LPOutputFormatter
from tests.assignments.date.helper import TestLPHelper


class TestLPOutputFormatter:

    helper = TestLPHelper()

    @pytest.mark.unit
    def test_get_result_with_groups(self):
        lp_solver_result = [
            ("group-1", "evaluator-10", "date-2-2-10"),
            ("group-2", "evaluator-11", "date-2-2-11"),
        ]

        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, groups, [])
        assert "2-2-10" == result.delivery_date_group(groups[0]).label()
        assert "2-2-11" == result.delivery_date_group(groups[1]).label()

    @pytest.mark.unit
    def test_get_result_with_evaluators(self):
        lp_solver_result = [
            ("group-1", "evaluator-10", "date-2-2-10"),
            ("group-2", "evaluator-11", "date-2-2-11"),
        ]

        num_evaluators = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, [], evaluators)
        assert "2-2-10" == result.delivery_date_evaluator(evaluators[0])[0].label()
        assert "2-2-11" == result.delivery_date_evaluator(evaluators[1])[0].label()

    @pytest.mark.unit
    def test_get_result_with_empty_result(self):
        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result([], groups, [])
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None

    @pytest.mark.unit
    def test_get_result_with_empty_groups(self):
        lp_solver_result = [
            ("group-1", "evaluator-10", "date-2-2-10"),
            ("group-2", "evaluator-11", "date-2-2-11"),
        ]

        num_groups = 2
        num_evaluators = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, [], evaluators)
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None

    @pytest.mark.unit
    def test_get_result_with_empty_evaluators(self):
        lp_solver_result = [
            ("group-1", "evaluator-10", "date-2-2-10"),
            ("group-2", "evaluator-11", "date-2-2-11"),
        ]

        num_groups = 2
        num_evaluators = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, groups, [])
        assert result.delivery_date_evaluator(evaluators[0]) == []
        assert result.delivery_date_evaluator(evaluators[1]) == []
