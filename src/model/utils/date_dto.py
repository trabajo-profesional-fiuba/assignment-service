class DateDto:

    def __init__(self, week, day, hr, priority = 0):
        self._week = week
        self._day = day
        self._hr = hr
        self._priority = priority

    @property
    def week(self):
        return self._week

    @property
    def day(self):
        return self._day

    @property
    def hr(self):
        return self._hr

    @property
    def priority(self):
        return self._priority

    def label(self):
        return f"{self._week}-{self._day}-{self._hr}"