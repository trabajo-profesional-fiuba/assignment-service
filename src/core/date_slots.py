from datetime import datetime


class DateSlot:

    def __init__(self, start_time: datetime) -> None:
        self.date = start_time

    def get_week(self) -> int:
        return self.date.isocalendar()[1]

    def get_day_of_week(self) -> int:
        return self.date.isoweekday()

    def get_hour(self) -> int:
        return self.date.hour

    def get_spanish_date(self):
        return self.date.strftime(f"%d de %b del %Y a las {self.get_hour()}hrs")

    def is_same_date(self, week, day, hour):
        is_same_date = True
        is_same_date = is_same_date and self.get_week() == week
        is_same_date = is_same_date and self.get_day_of_week() == day
        is_same_date = is_same_date and self.get_hour() == hour

        return is_same_date
