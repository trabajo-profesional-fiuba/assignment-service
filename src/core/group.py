from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from src.core.date_slots import DateSlot
from src.core.student import Student
from src.core.topic import Topic

if TYPE_CHECKING:
    from src.core.tutor import Tutor


class Group:

    def __init__(
        self, id: int, students: Optional[List[Student]] = None, group_number: int = 0
    ) -> None:
        self._id = id
        self._students = students if students is not None else []
        self._group_number = group_number

    @property
    def id(self) -> str:
        return self._id

    @property
    def group_number(self) -> str:
        return self._id


class UnassignedGroup(Group):
    """Representacion de un grupo que aun no tiene ni tema ni tutor asignados"""

    def __init__(
        self,
        id: int,
        students: Optional[List[Student]] = None,
        topics: Optional[List[Topic]] = None,
        group_number: int = 0,
    ) -> None:
        super().__init__(id=id, students=students, group_number=group_number)
        self._topics = topics if topics is not None else []

    @property
    def topics(self) -> str:
        return self._topics

    def preference_of(self, topic: Topic) -> int:
        topic_id = topic.id
        preference = next(
            (index + 1 for index, t in enumerate(self._topics) if t.id == topic_id), -1
        )
        return preference * 10 if preference >= 0 else 100


class AssignedGroup(Group):
    """Representacion de un grupo ya asignado a tema y tutor"""

    def __init__(
        self,
        id: int,
        tutor: Optional[Tutor] = None,
        available_dates: Optional[list[DateSlot]] = None,
        topic_assigned: Optional[Topic] = None,
        students: Optional[List[Student]] = None,
        reviewer_id: Optional[int] = None,
        group_number: int = 0,
    ) -> None:
        super().__init__(id=id, students=students, group_number=group_number)
        self._tutor = tutor
        self._available_dates = available_dates if available_dates is not None else []
        self._assigned_date = None
        self._assigned_topic = topic_assigned
        self._reviewer_id = reviewer_id

    @property
    def reviewer_id(self) -> int:
        return self._reviewer_id

    @property
    def available_dates(self) -> list[DateSlot]:
        return self._available_dates

    def emails(self) -> list[str]:
        return [student.email for student in self._students]

    def tutor_email(self) -> str:
        return self._tutor.email

    def assign_tutor(self, tutor: Tutor) -> None:
        self._tutor = tutor

    def assign_date(self, date: DateSlot):
        self._assigned_date = date

    def tutor_id(self) -> Optional[int]:
        return self._tutor.id if self._tutor else None

    def tutor_email(self) -> str:
        return self._tutor.email if self._tutor else None
