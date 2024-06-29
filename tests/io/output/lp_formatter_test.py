import pytest
from src.io.output.lp_formatter import LPOutputFormatter
from tests.assignments.date.helper import TestLPHelper
from src.io.output.result_context import ResultContext


class TestLPOutputFormatter:

    helper = TestLPHelper()

    @pytest.mark.skip
    def test_get_result_with_groups(self):
        # Arrange
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
        result_context = ResultContext(
            type="linear", result=lp_solver_result, groups=groups, evaluators=[]
        )

        formatter = LPOutputFormatter()

        # Act
        result = formatter.get_result(result_context)

        # Assert
        assert "2-2-10" == result.delivery_date_group(groups[0]).label()
        assert "2-2-11" == result.delivery_date_group(groups[1]).label()

    @pytest.mark.skip
    def test_get_result_with_evaluators(self):
        # Arrange
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
        result_context = ResultContext(
            type="linear", result=lp_solver_result, groups=[], evaluators=evaluators
        )

        formatter = LPOutputFormatter()

        # Act
        result = formatter.get_result(result_context)

        # Assert
        assert "2-2-10" == result.delivery_date_evaluator(evaluators[0])[0].label()
        assert "2-2-11" == result.delivery_date_evaluator(evaluators[1])[0].label()

    @pytest.mark.skip
    def test_get_result_with_empty_result(self):
        # Arrange
        num_groups = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        result_context = ResultContext(
            type="linear", result=[], groups=groups, evaluators=[]
        )

        formatter = LPOutputFormatter()

        # Act
        result = formatter.get_result(result_context)

        # Assert
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None

    @pytest.mark.skip
    def test_get_result_with_empty_groups(self):
        # Arrange
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
        result_context = ResultContext(
            type="linear", result=lp_solver_result, groups=[], evaluators=evaluators
        )
        formatter = LPOutputFormatter()

        # Act
        result = formatter.get_result(result_context)

        # Assert
        assert result.delivery_date_group(groups[0]) is None
        assert result.delivery_date_group(groups[1]) is None

    @pytest.mark.skip
    def test_get_result_with_empty_evaluators(self):

        # Arrange
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
        result_context = ResultContext(
            type="linear", result=lp_solver_result, groups=groups, evaluators=[]
        )

        # Act
        result = formatter.get_result(result_context)

        # Assert
        assert result.delivery_date_evaluator(evaluators[0]) == []
        assert result.delivery_date_evaluator(evaluators[1]) == []
