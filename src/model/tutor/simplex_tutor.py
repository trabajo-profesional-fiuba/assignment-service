from .tutor import Tutor


class SimplexTutor(Tutor):

    def __init__(self, id, avaliable_dates):
        super().__init__(id, 0, 0)
        self._avaliable_dates = avaliable_dates

    @property
    def avaliable_dates(self):
        return self._avaliable_dates
