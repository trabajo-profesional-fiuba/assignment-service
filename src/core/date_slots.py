from datetime import datetime


class DateSlot:

    def __init__(self, start_time: datetime) -> None:
        self._start_time = start_time

    def get_week(self) -> int:
        """Returns the number of wee of the year"""
        return self._start_time.isoweekday()

    def get_day_of_week(self) -> int:
        """Gets the day of the week, starting Monday: 1.."""
        return self._start_time.weekday() + 1

    def get_spanish_date(self):
        """Returns the number of wee of the year"""
        return self._start_time.strftime("%d de %b del %Y")
