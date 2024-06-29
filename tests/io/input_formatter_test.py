"""
import pandas as pd
import pytest

from src.io.input_formatter import InputFormatter
from src.exceptions import TutorNotFound
from src.io.calendar import Calendar


class TestInputFormatter:

    calendar = Calendar()

    @pytest.mark.unit
    def test_one_group_with_one_available_date(self):
        Testing that group has expected available date.
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == 1
        assert result[0].hour == 9

    @pytest.mark.unit
    def test_available_dates_no_data(self):
        Testing that group has none available date if there is no data.
        groups_data = {"Número de equipo": [1], "Apellido del tutor": ["Smith"]}
        tutors_df = pd.DataFrame({})
        groups_df = pd.DataFrame(groups_data)

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._available_dates(groups_df.iloc[0]) == []

    @pytest.mark.unit
    def test_one_group_with_multiple_dates_in_different_days(self):
        Testing that one group has available dates in different days.
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7, Martes 2/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == 1
        assert result[0].hour == 9

        assert result[1].week == 1
        assert result[1].day == 2
        assert result[1].hour == 9

    @pytest.mark.unit
    def test_one_group_with_multiple_dates_in_different_hours(self):
        Testing that one group has available dates in different hours.
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == 1
        assert result[0].hour == 9

        assert result[1].week == 1
        assert result[1].day == 1
        assert result[1].hour == 10

    @pytest.mark.unit
    def test_one_group_with_multiple_dates_in_different_weeks(self):
        Testing that one group has available dates in different weeks.
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert result[0].week == 1
        assert result[0].day == 1
        assert result[0].hour == 9

        assert result[1].week == 1
        assert result[1].day == 1
        assert result[1].hour == 10

    @pytest.mark.unit
    def test_one_group_with_no_available_date(self):
        Testing that group has not available dates.
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._available_dates(groups_df.iloc[0]) == []

    @pytest.mark.unit
    def test_groups_without_available_dates(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [No puedo]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": ["John Smith", "Robert Jones"],
                "Dirección de correo electrónico": [
                    "smith@fi.uba.ar",
                    "jones@fi.uba.ar",
                ],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._groups()
        assert result[0].id == 1
        assert result[0].available_dates() == []
        assert result[0].tutor.id == 2

        assert result[1].id == 2
        assert result[1].available_dates() == []
        assert result[1].tutor.id == 1

    @pytest.mark.unit
    def test_groups_with_available_dates(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": ["John Smith", "Robert Jones"],
                "Dirección de correo electrónico": [
                    "smith@fi.uba.ar",
                    "jones@fi.uba.ar",
                ],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._groups()
        assert result[0].id == 1
        assert result[0].available_dates()[0].week == 1
        assert result[0].available_dates()[0].day == 1
        assert result[0].available_dates()[0].hour == 9
        assert result[0].tutor.id == 2

        assert result[1].id == 2
        assert result[1].available_dates()[0].week == 1
        assert result[1].available_dates()[0].day == 1
        assert result[1].available_dates()[0].hour == 9
        assert result[1].tutor.id == 1

    @pytest.mark.unit
    def test_tutor_id_found(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Smith", "Jones"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("Smith") == 2
        assert formatter._tutor_id("Jones") == 1

    @pytest.mark.unit
    def test_tutor_id_border_case(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["John", "Johnson"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {"Nombre y Apellido": ["Robert John", "William Johnson"]}
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("John") == 1
        assert formatter._tutor_id("Johnson") == 2

    @pytest.mark.unit
    def test_tutor_id_with_sensitive_case(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["smith", "Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Will Smith", "Robert jones"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("smith") == 2
        assert formatter._tutor_id("Jones") == 1

    @pytest.mark.unit
    def test_tutor_id_with_blank_space(self):
        groups_data = {
            "Número de equipo": [1, 2],
            "Apellido del tutor": ["Smith ", "Jones "],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Will Smith", "Robert jones"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("Smith ") == 2
        assert formatter._tutor_id("Jones ") == 1

    @pytest.mark.unit
    def test_tutor_id_not_found(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Jones"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Robert Jones"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        with pytest.raises(TutorNotFound) as err:
            formatter._tutor_id("Smith")
        assert str(err.value) == "Tutor 'smith' not found."

    @pytest.mark.unit
    def test_same_tutor_id_with_diff_case(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Smith"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("Smith") == formatter._tutor_id("smith")

    @pytest.mark.unit
    def test_same_tutor_id_with_accent_mark(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smíth"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({"Nombre y Apellido": ["Smith"]})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._tutor_id("Smith") == formatter._tutor_id("smith")

    @pytest.mark.unit
    def test_one_evaluator_group_with_one_available_date(self, mocker):
        Testing that group has expected available date.
        mocker.patch(
            "src.io.input_formatter.EVALUATORS",
            ["mocked_name1", "mocked_name2", "mocked_name3"],
        )
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Fontela"],
            "Fecha de entrega del informe final": ["03/03/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)

        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": ["mocked_name1"],
                "Dirección de correo electrónico": ["mocked_name1@fi.uba.ar"],
                "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._evaluators()
        assert len(result) == 1
        assert result[0].id == 1
        assert len(result[0].available_dates) == 1
        assert result[0].available_dates[0].label() == "1-1-9"

    @pytest.mark.unit
    def test_one_evaluator_group_without_available_date(self, mocker):
        Testing that group has expected available date.
        mocker.patch(
            "src.io.input_formatter.EVALUATORS",
            ["mocked_name1", "mocked_name2", "mocked_name3"],
        )

        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["03/03/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": ["mocked_name1"],
                "Dirección de correo electrónico": ["mocked_name1@fi.uba.ar"],
                "Semana 1/7 [No puedo]": ["Lunes 1/7"],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._evaluators()
        assert len(result) == 1
        assert result[0].id == 1
        assert len(result[0].available_dates) == 0

    @pytest.mark.unit
    def test_none_evaluator(self, mocker):
        Testing that group has expected available date.
        mocker.patch(
            "src.io.input_formatter.EVALUATORS",
            ["mocked_name1", "mocked_name2", "mocked_name3"],
        )

        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": ["John Smith"],
                "Dirección de correo electrónico": ["smith@fi.uba.ar"],
                "Semana 1/7 [No puedo]": ["Lunes 1/7"],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._evaluators()
        assert len(result) == 0

    @pytest.mark.unit
    def test_all_evaluators(self, mocker):
        Testing that group has expected available date.
        mocker.patch(
            "src.io.input_formatter.EVALUATORS",
            ["mocked_name1", "mocked_name2", "mocked_name3"],
        )
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["03/03/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame(
            {
                "Nombre y Apellido": [
                    "mocked_name1",
                    "mocked_name2",
                    "mocked_name3",
                ],
                "Dirección de correo electrónico": [
                    "mocked_name1@fi.uba.ar",
                    "mocked_name2@fi.uba.ar",
                    "mocked_name3@fi.uba.ar",
                ],
                "Semana 1/7 [9 a 10]": ["Lunes 1/7", "Lunes 1/7", "Lunes 1/7"],
            }
        )

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._evaluators()
        assert len(result) == 3

    @pytest.mark.unit
    def test_possible_dates_with_one_week_and_one_hour(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._possible_dates()
        assert len(result) == 5
        assert result[0].label() == "1-1-9"
        assert result[1].label() == "1-2-9"
        assert result[2].label() == "1-3-9"
        assert result[3].label() == "1-4-9"
        assert result[4].label() == "1-5-9"

    @pytest.mark.unit
    def test_possible_dates_with_one_week_but_two_hours(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._possible_dates()
        assert len(result) == 10
        assert result[0].label() == "1-1-9"
        assert result[1].label() == "1-2-9"
        assert result[2].label() == "1-3-9"
        assert result[3].label() == "1-4-9"
        assert result[4].label() == "1-5-9"

        assert result[5].label() == "1-1-10"
        assert result[6].label() == "1-2-10"
        assert result[7].label() == "1-3-10"
        assert result[8].label() == "1-4-10"
        assert result[9].label() == "1-5-10"

    @pytest.mark.unit
    def test_possible_dates_with_two_weeks_and_two_hours(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 1/7 [10 a 11]": ["Lunes 1/7"],
            "Semana 8/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 8/7 [10 a 11]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._possible_dates()
        assert len(result) == 20
        assert result[0].label() == "1-1-9"
        assert result[1].label() == "1-2-9"
        assert result[2].label() == "1-3-9"
        assert result[3].label() == "1-4-9"
        assert result[4].label() == "1-5-9"

        assert result[5].label() == "1-1-10"
        assert result[6].label() == "1-2-10"
        assert result[7].label() == "1-3-10"
        assert result[8].label() == "1-4-10"
        assert result[9].label() == "1-5-10"

        assert result[10].label() == "2-1-9"
        assert result[11].label() == "2-2-9"
        assert result[12].label() == "2-3-9"
        assert result[13].label() == "2-4-9"
        assert result[14].label() == "2-5-9"

        assert result[15].label() == "2-1-10"
        assert result[16].label() == "2-2-10"
        assert result[17].label() == "2-3-10"
        assert result[18].label() == "2-4-10"
        assert result[19].label() == "2-5-10"

    @pytest.mark.unit
    def test_available_dates_with_all_filtered_dates(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["01/07/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        assert formatter._available_dates(groups_df.iloc[0]) == []

    @pytest.mark.unit
    def test_available_dates_with_some_filtered_dates(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["01/07/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 8/7 [9 a 10]": ["Lunes 8/7"],
            "Semana 15/7 [9 a 10]": ["Lunes 15/7, Martes 16/7, Miércoles 17/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert len(result) == 2
        assert result[0].label() == "3-2-9"
        assert result[1].label() == "3-3-9"

    @pytest.mark.unit
    def test_available_dates_with_diff_months(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["01/07/2024"],
            "Semana 1/7 [9 a 10]": ["Lunes 1/7"],
            "Semana 8/7 [9 a 10]": ["Lunes 8/7"],
            "Semana 15/7 [9 a 10]": ["Lunes 15/7, Martes 16/7"],
            "Semana 5/8 [9 a 10]": ["Lunes 15/7"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert len(result) == 2
        assert result[0].label() == "3-2-9"
        assert result[1].label() == "6-1-9"

    def test_available_dates_with_diff_months_border_case(self):
        groups_data = {
            "Número de equipo": [1],
            "Apellido del tutor": ["Smith"],
            "Fecha de entrega del informe final": ["01/07/2024"],
            "Semana 29/7 [9 a 10]": ["Miércoles 31/7, Jueves 1/8"],
        }
        groups_df = pd.DataFrame(groups_data)
        tutors_df = pd.DataFrame({})

        formatter = InputFormatter(groups_df, tutors_df, self.calendar)
        result = formatter._available_dates(groups_df.iloc[0])
        assert len(result) == 2
        assert result[0].label() == "5-3-9"
        assert result[1].label() == "5-4-9"
"""