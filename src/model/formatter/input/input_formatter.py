import pandas as pd
import numpy as np

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
        - WEEKS_DICT (dict): A dictionary mapping week descriptions to their
        corresponding week numbers.
        - DAYS_DICT (dict): A dictionary mapping day names to `Day`
        enumeration values.
        - HOURS_DICT (dict): A dictionary mapping time slots to `Hour`
        enumeration values.
    """

    WEEKS_DICT = {
        "Semana 1/7": 1,
        "Semana 8/7": 2,
        "Semana 15/7": 3,
        "Semana 22/7": 4,
        "Semana 29/7": 5,
        "Semana 5/8": 6,
        "Semana 12/8": 7,
    }

    DAYS_DICT = {
        "Lunes": Day.MONDAY,
        "Martes": Day.TUESDAY,
        "Miércoles": Day.WEDNESDAY,
        "Jueves": Day.THURSDAY,
        "Viernes": Day.FRIDAY,
    }

    HOURS_DICT = {
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

    def __init__(self, groups_df, tutors_df):
        """
        Constructs the necessary attributes for the InputFormatter object.

        Params:
            - df (pd.DataFrame): The DataFrame containing the input data
            to be formatted.
        """
        self._groups_df = groups_df
        self._tutors_df = tutors_df

    def _group_id(self, group_id: int):
        """
        Generates a group identifier.

        Params:
            - group_id (int): The group number.

        Returns (str): The formatted group identifier.
        """
        return GROUP_ID + str(group_id)

    def _tutor_id(self, tutor_surname: str, tutor_column: str, df):
        """
        Generates a tutor identifier.

        Params:
            - tutor_surname (str): The surname of the tutor.

        Returns (str): The formatted tutor identifier.

        Raises:
            - TutorNotFound: If the tutor surname is not found in the DataFrame.
        """
        tutors = df[tutor_column].unique()
        tutors.sort()
        index = np.where(tutors == tutor_surname)[0]
        if len(index) > 0:
            return TUTOR_ID + str(index[0] + 1)
        else:
            raise TutorNotFound(f"Tutor '{tutor_surname}' not found.")

    def _extract_week_hour_parts(self, column):
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

    def _process_day_values(self, value):
        """
        Processes the day values from a string.

        Params:
            - value (str): The string containing day values separated by commas.

        Returns (list): A list of day names.
        """
        days = value.split(",")
        return [day.strip().split(" ")[0].strip() for day in days]

    def create_week(self, week_part):
        """
        Retrieves the week part from the WEEKS_DICT.

        Params:
            - week_part (str): The key for the week part to retrieve.

        Returns:
            int: The corresponding week part from WEEKS_DICT.

        Raises:
            WeekNotFound: If the week part is not found in WEEKS_DICT.
        """
        try:
            return self.WEEKS_DICT[week_part]
        except KeyError:
            raise WeekNotFound(f"Week '{week_part}' not found in WEEKS_DICT")

    def create_day(self, day):
        """
        Retrieves the day from the DAYS_DICT.

        Params:
            - day (str): The key for the day to retrieve.

        Returns:
            str: The corresponding day from DAYS_DICT.

        Raises:
            DayNotFound: If the day is not found in DAYS_DICT.
        """
        try:
            return self.DAYS_DICT[day]
        except KeyError:
            raise DayNotFound(f"Day '{day}' not found in DAYS_DICT")

    def create_hour(self, hour_part):
        """
        Retrieves the hour part from the HOURS_DICT.

        Params:
            - hour_part (str): The key for the hour part to retrieve.

        Returns:
            str: The corresponding hour part from HOURS_DICT.

        Raises:
            HourNotFound: If the hour part is not found in HOURS_DICT.
        """
        try:
            return self.HOURS_DICT[hour_part]
        except KeyError:
            raise HourNotFound(f"Hour part '{hour_part}' not found in HOURS_DICT")

    def _create_delivery_date(self, week_part, day, hour_part):
        """
        Creates a DeliveryDate object.

        Params:
            - week_part (str): The week part extracted from the column name.
            - day (str): The day name.
            - hour_part (str): The hour part extracted from the column name.

        Returns (DeliveryDate): The DeliveryDate object created from the provided parts.

        Raises:
            WeekNotFound: If the week part is not found in WEEKS_DICT.
            DayNotFound: If the day is not found in DAYS_DICT.
            HourNotFound: If the hour part is not found in HOURS_DICT.
        """
        try:
            week = self.create_week(week_part)
            day = self.create_day(day)
            hour = self.create_hour(hour_part)
            return DeliveryDate(week, day, hour)
        except (WeekNotFound, DayNotFound, HourNotFound) as e:
            raise ValueError(f"Failed to create DeliveryDate: {e}")

    def _availability_dates(self, row: pd.Series):
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

    def groups(self):
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
                self._tutor_id(
                    x["Apellido del tutor"], "Apellido del tutor", self._groups_df
                ),
            ),
            axis=1,
        )
        return groups

    def tutors(self):
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
                self._tutor_id(
                    x["Nombre y Apellido"], "Nombre y Apellido", self._tutors_df
                ),
                self._availability_dates(x),
            ),
            axis=1,
        )
        return tutors
