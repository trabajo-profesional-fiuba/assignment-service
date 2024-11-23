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

        assert week == 49

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

        assert "15 de Oct del 2024 a las 0hrs" == spanish_date

    @pytest.mark.unit
    def test_get_hour_of_date(self):

        # Arrange
        date = DateSlot(start_time=datetime(2024, 10, 15, 10, 0, 0))

        # Arrange
        hour = date.get_hour()

        assert hour == 10

    @pytest.mark.parametrize(
        "week, day, hour, expected",
        [
            (49, 2, 10, True),
            (42, 5, 14, False),
        ],
    )
    @pytest.mark.unit
    def test_is_same_date(self, week, day, hour, expected):
        date = DateSlot(start_time=datetime(2024, 10, 15, 10, 0, 0))
        assert date.is_same_date(week, day, hour) == expected
