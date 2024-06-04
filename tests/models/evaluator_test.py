import pytest

from src.model.utils.evaluator import Evaluator
from src.model.utils.delivery_date import DeliveryDate


class TestEvaluator:

    @pytest.mark.unit
    def test_evaluator_has_empty_dates_if_they_are_not_passed(self):
        # Arrange
        evaluator = Evaluator(1)
        # Act
        available_dates = evaluator.available_dates
        # Assert
        assert len(available_dates) == 0

    @pytest.mark.unit
    def test_evaluator_dates_if_they_are_passed(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 4, 1), DeliveryDate(1, 3, 2)]
        evaluator = Evaluator(1, dates)
        # Act
        available_dates = evaluator.available_dates
        # Assert
        assert len(available_dates) == 3
