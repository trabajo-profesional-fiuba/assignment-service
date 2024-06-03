from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.topic import Topic


class Group:

    def __init__(self, id: int, tutor=None, state=None) -> None:
        self._id = id
        self._tutor = tutor
        self._state = state

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

    @property
    def tutor(self):
        return self._tutor
    
    @property
    def topics(self) -> list[Topic]:
        return self._state.topics

    @state.setter
    def state(self, state) -> None:
        self._state = state

    def assign(self, item) -> None:
        self.state.assign(item, self)

    def assign_tutor(self, tutor: Tutor) -> None:
        self._tutor = tutor

    def assign_date(self, date) -> None:
        self._state.assign_date(date)

    def is_tutored_by(self, tutor_id) -> bool:
        return self._tutor.id == tutor_id

    def add_available_dates(self, available_dates) -> None:
        final_state = FinalStateGroup(available_dates)
        self._state = final_state

    def preference_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        return self._state.preference_of(topic)
