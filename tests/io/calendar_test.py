import pytest
import pandas as pd

from src.io.calendar import Calendar
from src.exceptions import WeekNotFound
from src.model.utils.delivery_date import DeliveryDate


class TestCalendar:

    calendar = Calendar()

    @pytest.mark.unit
    def test_create_delivery_date_success(self):
        delivery_date = self.calendar._create_delivery_date(
            "Semana 1/7", "Lunes", "9 a 10"
        )
        assert delivery_date.week == 1
        assert delivery_date.day == 1
        assert delivery_date.hour == 9

    @pytest.mark.unit
    def test_create_delivery_date_week_not_found(self):
        with pytest.raises(ValueError) as exc_info:
            self.calendar._create_delivery_date("nonexistent_week", "Lunes", "9 a 10")
        assert "Week 'nonexistent_week' not found in WEEKS_dict" in str(exc_info.value)

    @pytest.mark.unit
    def test_create_delivery_date_day_not_found(self):
        with pytest.raises(ValueError) as exc_info:
            self.calendar._create_delivery_date(
                "Semana 1/7", "NonexistentDay", "9 a 10"
            )
        assert "Day 'NonexistentDay' not found in DAYS_dict" in str(exc_info.value)

    @pytest.mark.unit
    def test_create_delivery_date_hour_not_found(self):
        with pytest.raises(ValueError) as exc_info:
            self.calendar._create_delivery_date(
                "Semana 1/7", "Lunes", "nonexistent_hour"
            )
        assert "Hour part 'nonexistent_hour' not found in HOURS_dict" in str(
            exc_info.value
        )

    def test_extract_day_month_with_diff_days(self):
        weeks = [
            "Semana 1/7",
            "Semana 8/7",
            "Semana 15/7",
            "Semana 22/7",
            "Semana 29/7",
        ]
        for i, week in enumerate(weeks):
            result = self.calendar._extract_day_month(week)
            assert result[0] == 1 + (7 * i)
            assert result[1] == 7

    def test_extract_day_month_with_diff_months(self):
        weeks = ["Semana 1/7", "Semana 1/8", "Semana 1/9", "Semana 1/10", "Semana 1/11"]
        for i, week in enumerate(weeks):
            result = self.calendar._extract_day_month(week)
            assert result[0] == 1
            assert result[1] == 7 + i

    @pytest.mark.unit
    def test_get_day_month_from_value_with_real_data(self):
        weeks = [
            "Semana 1/7",
            "Semana 8/7",
            "Semana 15/7",
            "Semana 22/7",
            "Semana 29/7",
            "Semana 5/8",
            "Semana 12/8",
        ]
        for i, week in enumerate(weeks):
            assert week == self.calendar._get_day_month_from_value(i + 1)

    @pytest.mark.unit
    def test_get_day_month_from_value_when_week_not_found(self):
        with pytest.raises(WeekNotFound) as exc_info:
            self.calendar._get_day_month_from_value(9)
        assert "Week '9' not found in WEEKS_dict" in str(exc_info.value)

    @pytest.mark.unit
    def test_to_datetime_with_real_data(self):
        result = self.calendar._to_datetime(DeliveryDate(1, 1, 9))
        assert result.year == 2024
        assert result.month == 7
        assert result.day == 1

    @pytest.mark.unit
    def test_create_base_date_with_data(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["01/07/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)

        result = self.calendar._create_base_date(groups_df.iloc[0])
        assert result.year == 2024
        assert result.month == 7
        assert result.day == 15

    @pytest.mark.unit
    def test_create_base_date_without_data(self):
        assert self.calendar._create_base_date(None) is None
