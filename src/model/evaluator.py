class Evaluator:

    def __init__(self, id: str, available_dates: list):
        self._id = id
        self._available_dates = available_dates

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def available_dates(self):
        return self._available_dates

    def find_available_dates(self, dates: list):
        return list(set(dates) & set(self._available_dates))
