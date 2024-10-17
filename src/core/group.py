from typing import List, Optional
from src.core.date_slots import DateSlot
from src.core.student import Student
from src.core.tutor import Tutor
from src.core.topic import Topic


class Group:

    def __init__(
        self,
        id: int,
        tutor=None,
        students_emails: list[str] = None,
        reviewer_id: int = None,
    ) -> None:
        self._id = id
        self._tutor = tutor
        self._available_dates = []
        self._assigned_date = None
        self._topics = []
        self._assigned_topic = None
        self._students_emails = students_emails if students_emails is not None else []
        self._reviewer_id = reviewer_id

    @property
    def id(self) -> str:
        return self._id

    @property
    def reviewer_id(self) -> str:
        return self._reviewer_id

    @property
    def tutor(self):
        return self._tutor

    @property
    def students_emails(self):
        return self._students_emails

    @property
    def assigned_date(self):
        return self._assigned_date

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def assigned_topic(self):
        return self._assigned_topic

    @property
    def topics(self) -> list[Topic]:
        """
        Returns a list of topics.
        """
        return self._topics

    def add_topics(self, topics: list[Topic]):
        self._topics = topics

    def assign_topic(self, topic: Topic):
        self._assigned_topic = topic

    def preference_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        return self._topics[topic.id - 1].cost

    def assign_tutor(self, tutor: Tutor) -> None:
        self._tutor = tutor

    def is_tutored_by(self, tutor_id) -> bool:
        return self._tutor.id == tutor_id

    def add_available_dates(self, available_dates) -> None:
        self._available_dates = available_dates

    def assign_date(self, date):
        self._assigned_date = date

    def filter_dates(self, dates=[]):
        possible_dates = []
        for date in self._available_dates:
            if date.label() in dates:
                possible_dates.append(date)
        return [d.label() for d in self._available_dates]

    def cost_of_week(self, week):
        TOTAL_SLOTS_PER_WEEK = 5 * 11
        availability = len(
            list(filter(lambda x: (x.week == week), self._available_dates))
        )
        cost = TOTAL_SLOTS_PER_WEEK - availability
        return cost

    def cost_of_date(self, date):
        DAY_SLOTS = 11
        availability = len(
            list(filter(lambda x: (x.day == date.day), self._available_dates))
        )
        cost = DAY_SLOTS - availability
        return cost

    def tutor_email(self):
        if self._tutor:
            return self._tutor.email
        return None

    def tutor_id(self):
        if self._tutor:
            return self._tutor.id
        return None


class UnassignedGroup:
    """The base group only contains the id, Students and the Topics"""

    def __init__(
        self,
        id: int,
        students: Optional[List[Student]] = None,
        topics: Optional[List[Topic]] = None,
    ) -> None:
        self._id = id
        self._students = students if students is not None else []
        self._topics = topics if topics is not None else []

    @property
    def id(self) -> str:
        return self._id

    @property
    def topics(self) -> str:
        return self._topics

    def preference_of(self, topic: Topic) -> int:
        topic_id = topic.id
        preference = next(
            (index + 1 for index, t in enumerate(self._topics) if t.id == topic_id), -1
        )
        return (
            preference * 10 if preference >= 0 else 100
        )  # 100 es el costo de no querer ese topic.


class AssignedGroup:

    def __init__(
        self,
        id: int,
        tutor: Optional[Tutor] = None,
        available_dates: Optional[list[DateSlot]] = None,
        topic_assigned: Optional[Topic] = None,
        students: Optional[List[Student]] = None,
        reviewer_id: Optional[int] = None,
    ) -> None:
        self._id = id
        self._tutor = tutor
        self._available_dates = available_dates if available_dates is not None else []
        self._assigned_date = None
        self._topics = []
        self._assigned_topic = topic_assigned
        self._students = students if students is not None else []
        self._reviewer_id = reviewer_id
