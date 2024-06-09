import pandas as pd
import numpy as np
import os
from typing import Tuple
from dotenv import load_dotenv

from src.model.utils.delivery_date import DeliveryDate
from src.model.group.group import Group
from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.model.utils.evaluator import Evaluator
from src.constants import BLANK_SPACE
from src.exceptions import TutorNotFound, WeekNotFound, DayNotFound, HourNotFound

load_dotenv()
EVALUATORS = os.getenv("EVALUATORS", "").split(",")


def get_evaluators():
    return EVALUATORS


class InputFormatter:
    """
    A class used to format input data from a DataFrame for delivery scheduling.

    Attributes:
        - WEEKS_dict (dict): A dictionary mapping week descriptions to their
        corresponding week numbers.
        - DAYS_dict (dict): A dictionary mapping day names to their
        corresponding day numbers
        - HOURS_dict (dict): A dictionary mapping time slots to their
        corresponding hour numbers
    """

    WEEKS_dict = {
        "Semana 1/7": 1,
        "Semana 8/7": 2,
        "Semana 15/7": 3,
        "Semana 22/7": 4,
        "Semana 29/7": 5,
        "Semana 5/8": 6,
        "Semana 12/8": 7,
    }

    DAYS_dict = {
        "Lunes": 1,
        "lunes": 1,
        "Martes": 2,
        "martes": 2,
        "Miercoles": 3,
        "miercoles": 3,
        "Miércoles": 3,
        "jueves": 4,
        "Jueves": 4,
        "viernes": 5,
        "Viernes": 5,
    }

    HOURS_dict = {
        "9 a 10": 9,
        "10 a 11": 10,
        "11 a 12": 11,
        "12 a 13": 12,
        "14 a 15": 14,
        "15 a 16": 15,
        "16 a 17": 16,
        "17 a 18": 17,
        "18 a 19": 18,
        "19 a 20": 19,
        "20 a 21": 20,
    }

    def __init__(self, groups_df: pd.DataFrame, tutors_df: pd.DataFrame) -> None:
        """
        Constructs the necessary attributes for the InputFormatter object.

        Params:
            - df (pd.DataFrame): The DataFrame containing the input data
            to be formatted.
        """
        self._groups_df = groups_df
        self._tutors_df = tutors_df

    def _all_tutor_names(self) -> list[str]:
        tutors = self._tutors_df["Nombre y Apellido"].str.split().str[-1].str.strip()
        tutors = tutors.str.lower()
        tutors = tutors.unique()
        tutors.sort()
        return tutors

    def _has_blank_space(self, string: str) -> bool:
        return BLANK_SPACE in string

    def _format_lastname(self, lastname: str) -> str:
        if self._has_blank_space(lastname.strip()):
            aux = lastname.lower().split(BLANK_SPACE)
            lastname = aux[len(aux) - 1]
        return lastname.lower().strip()

    def _tutor_id(self, tutor_lastname: str) -> int:
        """
        Generates a unique tutor identifier based on their lastname.

        Params:
            - tutor_lastname (str): The lastname of the tutor.

        Returns (int): The tutor identifier.

        Raises:
            - TutorNotFound: If the tutor lastname is not found in the DataFrame.

        This method extracts the last name (assuming the last name is the last word
        of the full name) from the tutors DataFrame.
        It converts the last names to lowercase, gets the unique values of the last
        names, sorts the unique last names alphabetically.
        """
        tutors = self._all_tutor_names()
        tutor_lastname = self._format_lastname(tutor_lastname)
        index = np.where([tutor_lastname.lower() == tutor for tutor in tutors])[0]
        if len(index) > 0:
            return int(index[0] + 1)
        raise TutorNotFound(f"Tutor '{tutor_lastname}' not found.")

    def _extract_week_hour_parts(self, column: str) -> Tuple[str, str]:
        """
        Extracts the week part and hour part from a column name.

        Params:
            - column (str): The column name containing the week and hour information.

        Returns (tuple): A tuple containing the week part and hour part.
        """
        columns_parts = column.split("[")
        week_part = columns_parts[0].strip()
        hour_part = columns_parts[1].replace("]", "").strip()
        return week_part, hour_part

    def _process_day_values(self, value: str) -> list[str]:
        """
        Processes the day values from a string.

        Params:
            - value (str): The string containing day values separated by commas.

        Returns (list): A list of day names.
        """
        days = value.split(",")
        return [day.strip().split(" ")[0].strip() for day in days]

    def create_week(self, week_part: str) -> int:
        """
        Retrieves the week part from the WEEKS_dict.

        Params:
            - week_part (str): The key for the week part to retrieve.

        Returns:
            int: The corresponding week part from WEEKS_dict.

        Raises:
            WeekNotFound: If the week part is not found in WEEKS_dict.
        """
        try:
            return self.WEEKS_dict[week_part]
        except KeyError:
            raise WeekNotFound(f"Week '{week_part}' not found in WEEKS_dict")

    def create_day(self, day: str) -> int:
        """
        Retrieves the day from DAYS_dict.

        Params:
            - day (str): The key for the day to retrieve.

        Returns:
            int: The corresponding day from DAYS_dict.

        Raises:
            DayNotFound: If the day is not found in DAYS_dict.
        """
        try:
            return self.DAYS_dict[day]
        except KeyError:
            raise DayNotFound(f"Day '{day}' not found in DAYS_dict")

    def create_hour(self, hour_part: str) -> int:
        """
        Retrieves the hour part from the HOURS_dict.

        Params:
            - hour_part (str): The key for the hour part to retrieve.

        Returns:
            int: The corresponding hour part from HOURS_dict.

        Raises:
            HourNotFound: If the hour part is not found in HOURS_dict.
        """
        try:
            return self.HOURS_dict[hour_part]
        except KeyError:
            raise HourNotFound(f"Hour part '{hour_part}' not found in HOURS_dict")

    def _create_delivery_date(
        self, week_part: str, day: str, hour_part: str
    ) -> DeliveryDate:
        """
        Creates a DeliveryDate object.

        Params:
            - week_part (str): The week part extracted from the column name.
            - day (str): The day name.
            - hour_part (str): The hour part extracted from the column name.

        Returns (DeliveryDate): The DeliveryDate object created from the provided parts.

        Raises:
            WeekNotFound: If the week part is not found in WEEKS_dict.
            DayNotFound: If the day is not found in DAYS_dict.
            HourNotFound: If the hour part is not found in HOURS_dict.
        """
        try:
            week = self.create_week(week_part)
            day = self.create_day(day)
            hour = self.create_hour(hour_part)
            return DeliveryDate(week, day, hour)
        except (WeekNotFound, DayNotFound, HourNotFound) as e:
            raise ValueError(f"Failed to create DeliveryDate: {e}")

    def _available_dates(self, row: pd.Series) -> list[DeliveryDate]:
        """
        Extracts availability dates from a DataFrame row.

        Params:
            row (pd.Series): The row of the DataFrame containing availability data.

        Returns (list[DeliveryDate]): A list of `DeliveryDate` objects representing
        availability.
        """
        dates = []
        for column, value in row.items():
            if "Semana" in column:
                week_part, hour_part = self._extract_week_hour_parts(column)
                if hour_part != "No puedo" and not pd.isna(value):
                    days = self._process_day_values(value)
                    for day in days:
                        dates.append(
                            self._create_delivery_date(week_part, day, hour_part)
                        )
        return dates

    def _tutors(self) -> list[Tutor]:
        """
        Generates a list of `Tutor` objects from the DataFrame.

        Applies a lambda function to each row of the DataFrame `_df` to create
        a `Tutor` object with:
        - A tutor identifier generated by `_tutor_id`.
        - A tutor email.
        - A tutor name.
        - A FinalStateTutor with availability dates generated by `_available_dates`.

        Returns (list[Tutor]): A list of `Tutor` objects.
        """
        tutors = self._tutors_df.apply(
            lambda x: Tutor(
                self._tutor_id(x["Nombre y Apellido"]),
                x["Dirección de correo electrónico"],
                x["Nombre y Apellido"],
                state=FinalStateTutor(self._available_dates(x)),
            ),
            axis=1,
        )
        return tutors

    def _get_tutor_by_id(self, tutor_id: int) -> Tutor:
        for tutor in self._tutors():
            if tutor.id == tutor_id:
                return tutor
        raise TutorNotFound(f"Tutor '{tutor_id}' not found.")

    def _groups(self) -> list[Group]:
        """
        Generates a list of `Group` objects from the DataFrame.

        Applies a lambda function to each row of the DataFrame `_df` to create
        a `Group` object with:
        - A group identifier.
        - A `Tutor` generated by `_get_tutor_by_id`.
        - A `FinalStateGroup` state with a list of `AvailableDates`.

        Returns (list[Group]): A list of `Group` objects.
        """
        groups = self._groups_df.apply(
            lambda x: Group(
                x["Número de equipo"],
                tutor=self._get_tutor_by_id(self._tutor_id(x["Apellido del tutor"])),
                state=FinalStateGroup(self._available_dates(x)),
            ),
            axis=1,
        )
        return groups

    def _evaluators(self) -> list[Evaluator]:
        evaluators_df = self._tutors_df[
            self._tutors_df["Nombre y Apellido"].isin(get_evaluators())
        ]
        evaluators = evaluators_df.apply(
            lambda x: Evaluator(
                self._tutor_id(x["Nombre y Apellido"]),
                self._available_dates(x),
            ),
            axis=1,
        )
        return evaluators

    def _possible_dates(self) -> list[DeliveryDate]:
        """
        Extracts possible dates from a list of columns.

        Returns (list[DeliveryDate]): A list of `DeliveryDate` objects representing
        possible dates.
        """
        dates = []
        for column in self._groups_df.columns:
            if "Semana" in column:
                week_part, hour_part = self._extract_week_hour_parts(column)
                if hour_part != "No puedo":
                    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
                    for day in days:
                        dates.append(
                            self._create_delivery_date(week_part, day, hour_part)
                        )
        return dates

    def get_data(self):
        return (
            self._groups(),
            self._tutors(),
            self._evaluators(),
            self._possible_dates(),
        )
