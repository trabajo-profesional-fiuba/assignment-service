
import pytest
from datetime import datetime

from src.core.date_slots import DateSlot

class TestDateSlot:

    @pytest.mark.unit
    def test_get_week_of_date(self):

        # Arrange
        date = DateSlot(start_time=datetime(2002, 12, 4, 20, 0, 0))

        # Arrange
        week = date.get_week()

        assert week == 3

    @pytest.mark.unit
    def test_get_day_of_date(self):

        # Arrange
        date = DateSlot(start_time=datetime(2024, 10, 15, 0, 0, 0))

        # Arrange
        day = date.get_day_of_week()

        assert day == 2

    @pytest.mark.unit
    def test_translate_date_to_spanish(self):

        # Arrange
        date = DateSlot(start_time=datetime(2024, 10, 15, 0, 0, 0))

        # Arrange
        spanish_date = date.get_spanish_date()

        assert "15 de Oct del 2024" == spanish_date