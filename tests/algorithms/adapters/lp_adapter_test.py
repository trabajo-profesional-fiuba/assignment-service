import pytest
from src.core.algorithms.adapters.lp_adapter import LPAdapter
from tests.algorithms.date.helper import TestLPHelper
from src.core.algorithms.adapters.result_context import ResultContext


class TestLPAdapter:

    helper = TestLPHelper()

    @pytest.mark.unit
    def test_get_result_with_groups(self):
        # Arrange
        lp_solver_result = [
            ("group-1", "evaluator-10", "date-2-2-10"),
            ("group-2", "evaluator-11", "date-2-2-11"),
        ]

        # num_groups = 2
        # num_weeks = 4
        # days_per_week = [1, 2, 3, 4, 5]
        # hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        # dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        # groups = self.helper.create_groups(num_groups, dates)
        result_context = ResultContext(type="linear", result=lp_solver_result)

        formatter = LPAdapter()

        # Act
        result = formatter.adapt_results(result_context)

        # Assert
        assert "date-2-2-10" == result.get_results()[0][2]
        assert "date-2-2-11" == result.get_results()[1][2]

    @pytest.mark.unit
    def test_get_result_with_empty_result(self):
        # Arrange
        result_context = ResultContext(type="linear", result=[])

        formatter = LPAdapter()

        # Act
        result = formatter.adapt_results(result_context)

        # Assert
        assert len(result.get_results()) == 0
