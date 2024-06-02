from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor


class Group:

    def __init__(self, id, tutor=None):
        """When _ is used, that means is a private attribute"""
        self._id = id
        self._tutor = tutor
        self._state = None

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    """ This performs dinamic double-distpach
    """

    def assign(self, item):
        self.state.assign(item, self)

    def assign_tutor(self, tutor: Tutor):
        self._tutor = tutor

    def assign_date(self, date):
        self._state.assign_date(date)

    def is_tutored_by(tutor_id):
        return self._tutor.id == tutor_id

    def add_avaliable_dates(self, avaliable_dates):
        final_state = FinalStateGroup(avaliable_dates)
        self._state = final_state

    def filter_dates(self, dates: list):
        return self.state.filter_dates(dates)
