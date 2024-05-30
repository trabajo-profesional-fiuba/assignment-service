import pandas as pd
import pytest
from src.model.formatter.input.input_formatter import InputFormatter
from src.model.delivery_date.day import Day
from src.model.delivery_date.hour import Hour
from src.exceptions import TutorNotFound


class TestInputFormatter:

    @pytest.mark.formatter
    def test_one_group_with_one_availability_date(self):
        """Testing that group has expected availability date."""
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter._availability_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hour == Hour.H_9_10

    @pytest.mark.formatter
    def test_availability_dates_no_data(self):
        """Testing that group has none availability date if there is no data."""
        groups_data = {"Número de equipo": [1], "Apellido del tutor": ["Smith"]}
        tutors_df = pd.DataFrame({})
        groups_df = pd.DataFrame(groups_data)

        formatter = InputFormatter(groups_df, tutors_df)
        assert formatter._availability_dates(groups_df.iloc[0]) == []

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_days(self):
        """Testing that one group has availability dates in different days."""
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7, Martes 2/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter._availability_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hour == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.TUESDAY
        assert result[1].hour == Hour.H_9_10

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_hours(self):
        """Testing that one group has availability dates in different hours."""
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter._availability_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hour == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.MONDAY
        assert result[1].hour == Hour.H_10_11

    @pytest.mark.formatter
    def test_one_group_with_multiple_dates_in_different_weeks(self):
        """Testing that one group has availability dates in different weeks."""
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter._availability_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == Day.MONDAY
        assert result[0].hour == Hour.H_9_10

        assert result[1].week == 1
        assert result[1].day == Day.MONDAY
        assert result[1].hour == Hour.H_10_11

    @pytest.mark.formatter
    def test_one_group_with_no_availability_date(self):
        """Testing that group has not availability dates."""
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        assert formatter._availability_dates(groups_df.iloc[0]) == []

    @pytest.mark.formatter
    def test_groups_without_availability_dates(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter.groups()
        assert result[0].id == "g1"
        assert result[0].available_dates == []
        assert result[0].tutor_id == "p2"

        assert result[1].id == "g2"
        assert result[1].available_dates == []
        assert result[1].tutor_id == "p1"

    @pytest.mark.formatter
    def test_groups_with_availability_dates(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter.groups()
        assert result[0].id == "g1"
        assert result[0].available_dates[0].week == 1
        assert result[0].available_dates[0].day == Day.MONDAY
        assert result[0].available_dates[0].hour == Hour.H_9_10
        assert result[0].tutor_id == "p2"

        assert result[1].id == "g2"
        assert result[1].available_dates[0].week == 1
        assert result[1].available_dates[0].day == Day.MONDAY
        assert result[1].available_dates[0].hour == Hour.H_9_10
        assert result[1].tutor_id == "p1"

    @pytest.mark.formatter
    def test_tutor_id_found(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        assert formatter._tutor_id("Smith", "Apellido del tutor", groups_df) == "p2"
        assert formatter._tutor_id("Jones", "Apellido del tutor", groups_df) == "p1"

    @pytest.mark.formatter
    def test_tutor_id_not_found(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        with pytest.raises(TutorNotFound) as err:
            formatter._tutor_id("Smith", "Apellido del tutor", groups_df)
        assert str(err.value) == "Tutor 'Smith' not found."

    @pytest.mark.formatter
    def test_create_delivery_date_success(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        delivery_date = formatter._create_delivery_date("Semana 1/7", "Lunes", "9 a 10")
        assert delivery_date.week == 1
        assert delivery_date.day == Day.MONDAY
        assert delivery_date.hour == Hour.H_9_10

    @pytest.mark.formatter
    def test_create_delivery_date_week_not_found(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        with pytest.raises(ValueError) as exc_info:
            formatter._create_delivery_date("nonexistent_week", "Lunes", "9 a 10")
        assert "Week 'nonexistent_week' not found in WEEKS_DICT" in str(exc_info.value)

    @pytest.mark.formatter
    def test_create_delivery_date_day_not_found(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        with pytest.raises(ValueError) as exc_info:
            formatter._create_delivery_date("Semana 1/7", "NonexistentDay", "9 a 10")
        assert "Day 'NonexistentDay' not found in DAYS_DICT" in str(exc_info.value)

    @pytest.mark.formatter
    def test_create_delivery_date_hour_not_found(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        with pytest.raises(ValueError) as exc_info:
            formatter._create_delivery_date("Semana 1/7", "Lunes", "nonexistent_hour")
        assert "Hour part 'nonexistent_hour' not found in HOURS_DICT" in str(
            exc_info.value
        )

    @pytest.mark.formatter
    def test_tutors_without_availability_dates(self):
        tutors_data = {
            "Nombre y Apellido": ["John Smith"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7"],
        }
        tutors_df = pd.DataFrame(tutors_data)
        groups_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter.tutors()
        assert result[0].id == "p1"
        assert result[0].available_dates == []

    @pytest.mark.formatter
    def test_tutors_with_availability_dates(self):
        tutors_data = {
            "Nombre y Apellido": ["John Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        tutors_df = pd.DataFrame(tutors_data)
        groups_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df)
        result = formatter.tutors()
        assert result[0].id == "p1"
        assert result[0].available_dates[0].week == 1
        assert result[0].available_dates[0].day == Day.MONDAY
        assert result[0].available_dates[0].hour == Hour.H_9_10
