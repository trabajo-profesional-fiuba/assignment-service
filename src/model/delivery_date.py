class DeliveryDate:
    def __init__(self, week: int, day: str, hours: list):
        self._week = week
        self._day = day
        self._hours = hours

    @property
    def week(self):
        return self._week

    @property
    def day(self):
        return self._day

    @property
    def hours(self):
        return self._hours
