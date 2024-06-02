class DeliveryDate:

    def __init__(self, week, day, hour):
        self._week = week
        self._day = day
        self._hour = hour

    def label(self):
        return f"{self._week}-{self._day}-{self._hour}"
