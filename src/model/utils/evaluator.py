class Evaluator:
    def __init__(self, id, available_dates=[]):
        self._id = id
        self._available_dates = available_dates
        self._assigned_dates = []

    @property
    def id(self):
        return self._id

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def assigned_dates(self):
        return self._assigned_dates

    def filter_dates(self, dates):
        labels = [d.label() for d in self._available_dates]
        possible_dates = []
        for date in dates:
            if date.label() in labels:
                possible_dates.append(date)
        return possible_dates

    def assign_date(self, date):
        self._assigned_dates.append(date)
    
    def assign_dates(self, dates):
        for d in dates:
            self.assign_date(d)
