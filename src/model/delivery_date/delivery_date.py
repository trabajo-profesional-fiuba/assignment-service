from src.model.delivery_date.day import Day
from src.model.delivery_date.hour import Hour


class DeliveryDate:
    def __init__(self, week: int, day: Day, hour: Hour):
        self._week = week
        self._day = day
        self._hour = hour

    @property
    def week(self):
        return self._week

    @property
    def day(self):
        return self._day

    @property
    def hour(self):
        return self._hour
