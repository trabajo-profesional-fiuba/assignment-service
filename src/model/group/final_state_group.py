class FinalStateGroup:

    def __init__(self, available_dates):
        self._available_dates = available_dates
        self._assigned_date = None

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def assigned_date(self):
        return self._assigned_date

    def assign_date(self, date):
        self._assigned_date = date

    def filter_dates(self, dates=[]):
        possible_dates = []
        for date in self._available_dates:
            if date.label() in dates:
                possible_dates.append(date)
        return [d.label() for d in self._available_dates]

    def cost_of_week(self, week):
        TOTAL_SLOTS_PER_WEEK = 5 * 11
        availability = len(
            list(filter(lambda x: (x.week == week), self._available_dates))
        )
        cost = TOTAL_SLOTS_PER_WEEK - availability
        return cost

    def cost_of_date(self, date):
        DAY_SLOTS = 11
        availability = len(
            list(filter(lambda x: (x.day == date.day), self._available_dates))
        )
        cost = DAY_SLOTS - availability
        return cost
