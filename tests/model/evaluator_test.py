import pytest

from src.model.utils.evalutor import Evaluator

class TestEvaluator:

    @pytest.mark.unit
    def test_evaluator_has_empty_dates_if_they_are_not_passed(self):

        evaluator = Evaluator(1)

        avaliable_dates = evaluator.avaliable_dates

        assert len(avaliable_dates) == 0