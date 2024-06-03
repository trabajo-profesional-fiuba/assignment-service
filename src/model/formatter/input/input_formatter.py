import pandas as pd
import numpy as np
from typing import Tuple

from src.model.delivery_date.delivery_date import DeliveryDate
from src.model.delivery_date.hour import Hour
from src.model.delivery_date.day import Day
from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.constants import GROUP_ID, TUTOR_ID
from src.exceptions import TutorNotFound, WeekNotFound, DayNotFound, HourNotFound


class InputFormatter:
    """
    A class used to format input data from a DataFrame for delivery scheduling.

    Attributes:
        - WEEKS_dict (dict): A dictionary mapping week descriptions to their
        corresponding week numbers.
        - DAYS_dict (dict): A dictionary mapping day names to `Day`
        enumeration values.
        - HOURS_dict (dict): A dictionary mapping time slots to `Hour`
        enumeration values.
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
        "Lunes": Day.MONDAY,
        "Martes": Day.TUESDAY,
        "Miércoles": Day.WEDNESDAY,
        "Jueves": Day.THURSDAY,
        "Viernes": Day.FRIDAY,
    }

    HOURS_dict = {
        "9 a 10": Hour.H_9_10,
        "10 a 11": Hour.H_10_11,
        "11 a 12": Hour.H_11_12,
        "12 a 13": Hour.H_12_13,
        "14 a 15": Hour.H_14_15,
        "15 a 16": Hour.H_15_16,
        "16 a 17": Hour.H_16_17,
        "17 a 18": Hour.H_17_18,
        "18 a 19": Hour.H_18_19,
        "19 a 20": Hour.H_19_20,
        "20 a 21": Hour.H_20_21,
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

    def _group_id(self, group_id: int) -> str:
        """
        Generates a group identifier.

        Params:
            - group_id (int): The group number.

        Returns (str): The formatted group identifier.
        """
        return GROUP_ID + str(group_id)

    def _tutor_id(self, tutor_lastname: str) -> str:
        """
        Generates a unique tutor identifier based on their lastname.

        Params:
            - tutor_lastname (str): The lastname of the tutor.

        Returns (str): The formatted tutor identifier.

        Raises:
            - TutorNotFound: If the tutor lastname is not found in the DataFrame.

        This method extracts the last name (assuming the last name is the last word
        of the full name) from the tutors DataFrame.
        It converts the last names to lowercase, gets the unique values of the last
        names, sorts the unique last names alphabetically.
        """
        tutors = self._tutors_df["Nombre y Apellido"].str.split().str[-1].str.strip()
        tutors = tutors.str.lower()
        tutors = tutors.unique()
        tutors.sort()
        index = np.where([tutor_lastname.lower() in tutor for tutor in tutors])[0]
        if len(index) > 0:
            return TUTOR_ID + str(index[0] + 1)
        else:
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

    def create_day(self, day: str) -> Day:
        """
        Retrieves the day from the DAYS_dict.

        Params:
            - day (str): The key for the day to retrieve.

        Returns:
            str: The corresponding day from DAYS_dict.

        Raises:
            DayNotFound: If the day is not found in DAYS_dict.
        """
        try:
            return self.DAYS_dict[day]
        except KeyError:
            raise DayNotFound(f"Day '{day}' not found in DAYS_dict")

    def create_hour(self, hour_part: str) -> Hour:
        """
        Retrieves the hour part from the HOURS_dict.

        Params:
            - hour_part (str): The key for the hour part to retrieve.

        Returns:
            str: The corresponding hour part from HOURS_dict.

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

    def _availability_dates(self, row: pd.Series) -> list[DeliveryDate]:
        """
        Extracts availability dates from a DataFrame row.

        Params:
            row (pd.Series): The row of the DataFrame containing availability data.

        Returns (list): A list of DeliveryDate objects representing availability.
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

    def groups(self) -> list[FinalStateGroup]:
        """
        Generates a list of `FinalStateGroup` objects from the DataFrame.

        Applies a lambda function to each row of the DataFrame `_df` to create
        a `FinalStateGroup` object with:
        - A group identifier generated by `_group_id`.
        - Availability dates generated by `_availability_dates`.
        - A tutor identifier generated by `_tutor_id`.

        Returns (pd.Series): A series of `FinalStateGroup` objects.
        """
        groups = self._groups_df.apply(
            lambda x: FinalStateGroup(
                self._group_id(x["Número de equipo"]),
                self._availability_dates(x),
                self._tutor_id(x["Apellido del tutor"]),
            ),
            axis=1,
        )
        return groups

    def tutors(self) -> list[FinalStateTutor]:
        """
        Generates a list of `FinalStateTutor` objects from the DataFrame.

        Applies a lambda function to each row of the DataFrame `_df` to create
        a `FinalStateTutor` object with:
        - A tutor identifier generated by `_tutor_id`.
        - Availability dates generated by `_availability_dates`.

        Returns (pd.Series): A series of `FinalStateTutor` objects.
        """
        tutors = self._tutors_df.apply(
            lambda x: FinalStateTutor(
                self._tutor_id(x["Nombre y Apellido"]),
                self._availability_dates(x),
            ),
            axis=1,
        )
        return tutors
