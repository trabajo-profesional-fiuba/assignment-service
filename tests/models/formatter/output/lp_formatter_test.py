import pytest
from src.model.formatter.output.lp_formatter import LPOutputFormatter
from tests.algorithms.date_simplex.helper import TestLPHelper


class TestLPOutputFormatter:

    helper = TestLPHelper()

    @pytest.mark.formatter
    def test_get_result_with_data(self):
        lp_solver_result = [(1, 10, 2, 2, 1), (2, 12, 2, 2, 1)]

        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, groups)
        assert "10-2-2" == result.delivery_date(groups[0]).label()
        assert "12-2-2" == result.delivery_date(groups[1]).label()

    @pytest.mark.formatter
    def test_get_result_with_empty_result(self):
        lp_solver_result = []

        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, groups)
        assert result.delivery_date(groups[0]) is None
        assert result.delivery_date(groups[1]) is None

    @pytest.mark.formatter
    def test_get_result_with_empty_groups(self):
        lp_solver_result = [(1, 10, 2, 2, 1), (2, 12, 2, 2, 1)]

        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)

        formatter = LPOutputFormatter()
        result = formatter.get_result(lp_solver_result, [])
        assert result.delivery_date(groups[0]) is None
        assert result.delivery_date(groups[1]) is None
