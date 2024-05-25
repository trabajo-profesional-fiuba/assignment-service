from .tutor import Tutor


class FinalStateTutor(Tutor):

    def __init__(self, id, available_dates):
        super().__init__(id, 0, 0)
        self._available_dates = available_dates

    @property
    def available_dates(self):
        return self._available_dates
