from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from src.core.date_slots import DateSlot
from src.core.topic import Topic

if TYPE_CHECKING:
    from src.core.group import AssignedGroup


class Tutor:
    """
    Esta clase representa a un tutor como un solo cuatrimestre,
    lo que significa que abstraemos los otros cuatrimestres del tutor y lo consideramos como un tutor
    por cuatrimestre.
    De esta manera, los algoritmos no tienen conocimiento de los otros cuatrimestres de ese tutor.
    """

    def __init__(
        self,
        id: int,
        name: str,
        last_name: str,
        email: str,
        capacity: int = 0,
        period_id: Optional[int] = None,
        topics: Optional[List[Topic]] = None,
        groups: Optional[List[AssignedGroup]] = None,
        available_dates: Optional[list[DateSlot]] = None,
        is_evaluator: bool = False,
    ):
        self._id = id
        self._name = name
        self._last_name = last_name
        self._is_evaluator = is_evaluator
        self._capacity = capacity
        self._topics = topics if topics else []
        self._email = email
        self._period_id = period_id
        self._groups = groups if groups else []
        self._available_dates = available_dates if available_dates is not None else []
        self._dates_assigned = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def period_id(self) -> str:
        return self._period_id

    @property
    def topics(self) -> str:
        return self._topics

    @property
    def capacity(self):
        return self._capacity

    @property
    def email(self) -> str:
        return self._email

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def groups(self) -> List[AssignedGroup]:
        return self._groups

    @property
    def available_dates(self) -> list[DateSlot]:
        return self._available_dates

    @available_dates.setter
    def available_dates(self, available_dates: list[DateSlot]):
        self._available_dates = available_dates

    def topics_ids(self):
        return [topic.id for topic in self._topics]

    def capacity_of(self, topic: Topic) -> int:
        matching_topic = next((t for t in self._topics if t.id == topic.id), None)
        if matching_topic is None:
            return 0
        return matching_topic.capacity

    def assign_groups(self, groups: list[AssignedGroup]):
        self._groups.extend(groups)

    def assign_date(self, date: DateSlot):
        self._dates_assigned.append(date)
