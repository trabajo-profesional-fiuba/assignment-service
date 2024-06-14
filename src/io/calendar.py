from datetime import timedelta, datetime

from src.model.utils.delivery_date import DeliveryDate
from src.exceptions import WeekNotFound, DayNotFound, HourNotFound


class Calendar:

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
        "lunes": 1,
        "martes": 2,
        "miercoles": 3,
        "jueves": 4,
        "viernes": 5,
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

    def __init__(self):
        pass

    def _extract_week_hour_parts(self, column: str) -> tuple[str, str]:
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
            return self.DAYS_dict[day.lower()]
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

    def _extract_day_month(self, week_string: str) -> tuple[int, int]:
        """
        Extracts the day and month numbers from a string formatted as 'Semana X/Y'.

        Args:
            week_string (str): The string containing the day and month numbers.

        Returns:
            tuple[int, int]: A tuple containing the day number and the month
            number as integers.
        """
        # Remove the 'Semana ' prefix and split by '/'
        _, day_month_part = week_string.split(" ")
        day, month = day_month_part.split("/")
        return int(day), int(month)

    def _get_day_month_from_value(self, week: int) -> str:
        """
        Gets the day and month string corresponding to a given week number.

        Args:
            week (int): The week number to look up.

        Returns:
            str: The day and month string corresponding to the week number.

        Raises:
            WeekNotFound: If the week is not found in WEEKS_dict.
        """
        for day_month, value in self.WEEKS_dict.items():
            if value == week:
                return day_month
        raise WeekNotFound(f"Week '{week}' not found in WEEKS_dict")

    def _calculate_datetime(
        self, year: int, month: int, start_day: int, additional_days: int
    ) -> datetime:
        """
        Calculate the correct datetime object based on the initial day and
        additional days.

        Args:
            year (int): The year for the datetime.
            month (int): The starting month.
            start_day (int): The initial day of the month.
            additional_days (int): The additional days to add to the start_day.

        Returns:
            datetime: The calculated datetime object.
        """
        initial_date = datetime(year, month, start_day)
        final_date = initial_date + timedelta(days=additional_days - 1)
        return final_date

    def _to_datetime(self, date: DeliveryDate) -> datetime:
        """
        Convert a DeliveryDate object to a datetime object.

        Args:
            date (DeliveryDate): The DeliveryDate object containing the week
            and day information.

        Returns:
            datetime: The corresponding datetime object for the given DeliveryDate.
        """
        # Get the initial day and month from the week value
        day, month = self._extract_day_month(self._get_day_month_from_value(date.week))
        # Calculate and return the correct datetime
        return self._calculate_datetime(2024, month, day, date.day)

    def _create_base_date(self, row) -> datetime:
        """
        Calculates the limit date which is two weeks from the final report delivery date.

        Params:
            row (pandas.Series): The row containing the final report delivery date.

        Returns:
            datetime: The calculated limit date.
        """
        if row is not None:
            columns = row.index
            if "Fecha de entrega del informe final" in columns:
                date = row["Fecha de entrega del informe final"]
                return datetime.strptime(date, "%d/%m/%Y") + timedelta(weeks=2)
        return None
