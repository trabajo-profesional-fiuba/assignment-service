from .group import Group

class FinalStateGroup(Group):

    def __init__(self, group_id, available_dates, tutor_id):
        super().__init__(group_id, 0)
        self._available_dates = available_dates
        self._tutor_id = tutor_id
        self._evaluation_date = None

    def set_evaluation_date(self, date):
        self._evaluation_date = date

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def evaluation_date(self):
        return self._evaluation_date

    @property
    def tutor_id(self):
        return self._tutor_id

    def find_tutor(self, tutors):
        """Find tutor for current group"""

        for t in tutors:
            if t._id == self._tutor_id:
                return t
