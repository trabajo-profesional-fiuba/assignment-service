import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import unicodedata
import datetime

from src.model.utils.delivery_date import DeliveryDate
from src.model.group.group import Group
from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.model.utils.evaluator import Evaluator
from src.exceptions import TutorNotFound
from src.io.calendar import Calendar

load_dotenv()
EVALUATORS = os.getenv("EVALUATORS", "").split(",")


def get_evaluators():
    return EVALUATORS


class InputFormatter:

    def __init__(
        self, groups_df: pd.DataFrame, tutors_df: pd.DataFrame, calendar: Calendar
    ) -> None:
        """
        Constructs the necessary attributes for the InputFormatter object.

        Params:
            - df (pd.DataFrame): The DataFrame containing the input data
            to be formatted.
        """
        self._groups_df = groups_df
        self._tutors_df = tutors_df
        self._calendar = calendar

    def _all_tutor_names(self) -> list[str]:
        tutors = self._tutors_df["Nombre y Apellido"].str.split().str[-1].str.strip()
        tutors = tutors.str.lower()
        tutors = tutors.unique()
        tutors.sort()
        return tutors

    def _format_lastname(self, lastname: str) -> str:
        return lastname.strip().lower().split(" ")[-1]

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

    def remove_accents(self, text: str) -> str:
        """
        Removes accents from a string and converts it to lowercase.

        This function normalizes the input string to decompose combined characters
        into their base characters and diacritics, then removes the diacritics.
        It also converts the string to lowercase and trims any leading or trailing
        whitespace.

        Params:
            text (str): The input string from which to remove accents.

        Returns:
            str: The processed string without accents and in lowercase.
        """
        # Normalize the text to decompose combined characters
        text = unicodedata.normalize("NFKD", text)
        # Remove diacritical marks (accents)
        text = "".join(c for c in text if not unicodedata.combining(c))
        # Convert to lowercase and strip leading/trailing whitespace
        return text.lower().strip()

    def _available_dates(self, row: pd.Series) -> list[DeliveryDate]:
        """
        Extracts availability dates from a DataFrame row.

        This method parses a row of the DataFrame to extract availability data,
        converting it into a list of `DeliveryDate` objects. It filters out dates
        that fall within two weeks of a base date (if provided).

        Params:
            row (pd.Series): The row of the DataFrame containing availability data.

        Returns:
            list[DeliveryDate]: A list of `DeliveryDate` objects representing
            availability.
        """
        dates = []
        base_date = self._calendar._create_base_date(row)

        for column, value in row.items():
            if self._is_valid_week_column(column):
                week_part, hour_part = self._calendar._extract_week_hour_parts(column)

                if self._is_valid_hour_part(hour_part):
                    dates.extend(
                        self._process_days(value, week_part, hour_part, base_date)
                    )

        return dates

    def _is_valid_week_column(self, column: str) -> bool:
        """
        Checks if the column name indicates a valid week.

        Params:
            column (str): The column name to check.

        Returns:
            bool: True if the column name contains "Semana", False otherwise.
        """
        return "Semana" in column

    def _process_days(
        self, value: str, week_part: str, hour_part: str, base_date: datetime
    ) -> list[DeliveryDate]:
        """
        Processes the day values and creates DeliveryDate objects.

        Params:
            value (str): The cell value containing the day information.
            week_part (str): The week part extracted from the column name.
            hour_part (str): The hour part extracted from the column name.
            base_date (datetime): The base date to filter dates against.

        Returns:
            list[DeliveryDate]: A list of `DeliveryDate` objects.
        """
        days = self._calendar._process_day_values(value)
        dates = []

        for day in days:
            delivery_date = self._calendar._create_delivery_date(
                week_part, self.remove_accents(day), hour_part
            )

            if self._is_date_valid(delivery_date, base_date):
                dates.append(delivery_date)

        return dates

    def _is_date_valid(self, delivery_date: DeliveryDate, base_date: datetime) -> bool:
        """
        Checks if a DeliveryDate object is valid based on the base date.

        Params:
            delivery_date (DeliveryDate): The DeliveryDate object to check.
            base_date (datetime): The base date to filter dates against.

        Returns:
            bool: True if the delivery_date is valid, False otherwise.
        """
        if base_date:
            return self._calendar._to_datetime(delivery_date) > base_date
        return True

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

    def _is_valid_hour_part(self, hour_part: str) -> bool:
        """
        Checks if an hour part is valid for delivery.

        Params:
            hour_part (str): The hour part extracted from the column name.

        Returns:
            bool: True if the hour part is not "No puedo", False otherwise.
        """
        return hour_part != "No puedo"

    def _is_week_column(self, column: str) -> bool:
        """
        Checks if a column name indicates a delivery week.

        Params:
            column (str): The column name to check.

        Returns:
            bool: True if the column name contains "Semana", False otherwise.
        """
        return "Semana" in column

    def _valid_week_days(self) -> list[str]:
        """
        Retrieves valid week days for delivery.

        Returns:
            list[str]: A list of valid week days ("Lunes" to "Viernes").
        """
        return ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    def _possible_dates(self) -> list[DeliveryDate]:
        """
        Extracts possible delivery dates from the columns of `_groups_df`.

        This method iterates through each column in `_groups_df` to identify columns
        related to delivery dates (indicated by containing "Semana"). It then extracts
        possible delivery dates for each valid day of the week (Monday to Friday),
        considering the hours specified for each day.

        Returns:
            list[DeliveryDate]: A list of `DeliveryDate` objects representing possible
            delivery dates.
        """
        dates = []

        for column in self._groups_df.columns:
            if self._is_week_column(column):
                week_part, hour_part = self._calendar._extract_week_hour_parts(column)
                if self._is_valid_hour_part(hour_part):
                    for day in self._valid_week_days():
                        delivery_date = self._calendar._create_delivery_date(
                            week_part, self.remove_accents(day).lower(), hour_part
                        )
                        dates.append(delivery_date)

        return dates

    def get_data(self):
        return (
            self._groups(),
            self._tutors(),
            self._evaluators(),
            self._possible_dates(),
        )
