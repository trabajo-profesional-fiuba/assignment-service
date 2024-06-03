from src.model.tutor.tutor import Tutor


class FinalStateTutor(Tutor):

    def __init__(self, id: str, email: str, name: str, available_dates: list):
        super().__init__(id, email, name)
        self._available_dates = available_dates
        self._assigned_dates = []

    def assign_date(self, date):
        self._assigned_dates.append(date)

    @property
    def available_dates(self):
        return self._available_dates
