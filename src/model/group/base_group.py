from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor


class Group:

    def __init__(self, id, tutor=None):
        self._id = id
        self._tutor = tutor
        self._state = None

    @property
    def id(self) -> str:
        """
        Retrieves the identifier of the group.

        Returns:
            str: The identifier of the group.
        """
        return self._id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def assign(self, item):
        self.state.assign(item, self)

    def assign_tutor(self, tutor: Tutor):
        self._tutor = tutor

    def assign_date(self, date):
        self._state.assign_date(date)

    def is_tutored_by(self, tutor_id):
        return self._tutor.id == tutor_id

    def add_available_dates(self, available_dates):
        final_state = FinalStateGroup(available_dates)
        self._state = final_state
