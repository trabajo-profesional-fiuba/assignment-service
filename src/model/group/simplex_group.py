from .group import Group


class SimplexGroup(Group):

    def __init__(self, group_id, avaliable_dates, tutor_id):
        super().__init__(group_id, 0)
        self._avaliable_dates = avaliable_dates
        self._tutor_id = tutor_id

    @property
    def avaliable_dates(self):
        return self._avaliable_dates

    def find_tutor(self, tutors):
        """Find tutor for current group"""

        for t in tutors:
            if t._id == self._tutor_id:
                return t
