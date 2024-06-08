from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.tutor import Tutor
from src.model.topic import Topic
from src.model.utils.delivery_date import DeliveryDate


class Group:

    def __init__(self, id: int, tutor=None, state=None) -> None:
        self._id = id
        self._tutor = tutor
        self._state = state

    @property
    def id(self) -> str:
        return self._id

    @property
    def tutor(self):
        return self._tutor

    @property
    def state(self):
        return self._state

    @property
    def topics(self) -> list[Topic]:
        return self._state.topics

    @state.setter
    def state(self, state) -> None:
        self._state = state

    def assign_tutor(self, tutor: Tutor) -> None:
        self._tutor = tutor

    def assign_date(self, date) -> None:
        self._tutor.assign_date(date)
        self._state.assign_date(date)

    def is_tutored_by(self, tutor_id) -> bool:
        return self._tutor.id == tutor_id

    def add_available_dates(self, available_dates) -> None:
        final_state = FinalStateGroup(available_dates)
        self._state = final_state

    def available_dates(self) -> list[DeliveryDate]:
        return self._state.available_dates

    def preference_of(self, topic: Topic) -> int:
        return self._state.preference_of(topic)

    def remove_dates(self, dates) -> None:
        self.state.remove_dates(dates)

    def assigned_date(self) -> str:
        return self._state.assigned_date

    def filter_dates(self, dates):
        tutor_dates = self._tutor.available_dates()
        return self._state.filter_dates(tutor_dates, dates)

    def cost_of_week(self, week):
        return self._state.cost_of_week(week)

    def cost_of_date(self, date):
        return self._state.cost_of_date(date)