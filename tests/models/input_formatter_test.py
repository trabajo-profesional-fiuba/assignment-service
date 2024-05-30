import pandas as pd
import pytest
from src.model.formatter.input_formatter import InputFormatter
from src.model.day import Day
from src.model.hour import Hour


class TestInputFormatter:

    @pytest.mark.formatter
    def test_one_group_with_one_availability_date(self):
        """Testing that group has expected availability date."""
        data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)

        result = formatter._availability_dates(df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hours == Hour.H_9_10

    @pytest.mark.formatter
    def test_availability_dates_no_data(self):
        """Testing that group has none availability date if there is no data."""
        data = {"Número de equipo": [1], "Apellido del tutor": ["Smith"]}
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)

        assert formatter._availability_dates(df.iloc[0]) == []

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_days(self):
        """Testing that one group has availability dates in different days."""
        data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7, Martes 2/7"],
        }
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)

        result = formatter._availability_dates(df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hours == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.TUESDAY
        assert result[1].hours == Hour.H_9_10

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_hours(self):
        """Testing that one group has availability dates in different hours."""
        data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)

        result = formatter._availability_dates(df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hours == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.MONDAY
        assert result[1].hours == Hour.H_10_11

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_weeks(self):
        """Testing that one group has availability dates in different weeks."""
        data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)

        result = formatter._availability_dates(df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hours == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.MONDAY
        assert result[1].hours == Hour.H_10_11

    @pytest.mark.formatter
    def test_one_group_with_no_availability_date(self):
        """Testing that group has not availability dates."""
        data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7"],
        }
        df = pd.DataFrame(data)
        formatter = InputFormatter(df)
        assert formatter._availability_dates(df.iloc[0]) == []

    @pytest.mark.formatter
    def test_groups_without_availability_dates(self):
        data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7", "Lunes 1/7"],
        }
        df = pd.DataFrame(data)

        formatter = InputFormatter(df)
        result = formatter.groups()

        assert result[0].id == "g1"
        assert result[0].available_dates == []
        assert result[0].tutor_id == "p1"

        assert result[1].id == "g2"
        assert result[1].available_dates == []
        assert result[1].tutor_id == "p2"

    @pytest.mark.formatter
    def test_groups_with_availability_dates(self):
        data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        df = pd.DataFrame(data)

        formatter = InputFormatter(df)
        result = formatter.groups()

        assert result[0].id == "g1"
        assert result[0].available_dates[0].week == 1
        assert result[0].available_dates[0].day == Day.MONDAY
        assert result[0].available_dates[0].hours == Hour.H_9_10
        assert result[0].tutor_id == "p1"

        assert result[1].id == "g2"
        assert result[1].available_dates[0].week == 1
        assert result[1].available_dates[0].day == Day.MONDAY
        assert result[1].available_dates[0].hours == Hour.H_9_10
        assert result[1].tutor_id == "p2"
