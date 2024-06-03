class Evaluator:
    def __init__(self, id, available_dates=[]):
        self._id = id
        self._available_dates = available_dates

    @property
    def id(self):
        return self._id

    @property
    def available_dates(self):
        return self._available_dates
