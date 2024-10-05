from src.core.delivery_date import DeliveryDate
from src.core.topic import Topic


class Tutor:
    """
    This class represents a Tutor during a specific Period.
    Although a tutor may be active in multiple periods, this abstraction considers each
    tutor within the context of a single period.
    Thus, each period has its tutors as a subset of objects that exist only within that
    period.
    """

    def __init__(
        self,
        id: int,
        email: str,
        name: str,
        last_name: str,
        capacity: int = 0,
        groups=None,
        topics=None,
        is_evaluator=False,
    ):
        self._id = id
        self._name = name
        self._last_name = last_name
        self._email = email
        self._available_dates = []
        self._as_tutor_dates = []
        self._as_evaluator_dates = []
        self._substitute_dates = []
        self._is_evaluator = is_evaluator
        self._capacity = capacity
        self._groups = groups
        self._topics = topics

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def as_tutor_dates(self):
        return self._as_tutor_dates

    @property
    def as_evaluator_dates(self):
        return self._as_evaluator_dates

    @property
    def substitute_dates(self):
        return self._substitute_dates

    @property
    def groups(self):
        return self._groups

    @property
    def topics(self):
        return self._topics

    @property
    def capacity(self):
        return self._capacity

    def set_capacity(self, capacity):
        self._capacity = capacity

    # def add_groups(self, groups: list["group.Group"]):
    #     self._groups = groups

    def add_groups(self, groups):
        if self._groups is None:
            self._groups = []
        for group in groups:
            group.assign_tutor(self)
            self._groups.append(group)

    def is_evaluator(self):
        return self._is_evaluator

    def groups_ids(self):
        return [g.id for g in self._groups]

    def topics_ids(self):
        return [t.id for t in self._topics]

    def make_evaluator(self):
        self._is_evaluator = True

    # Date manipulations
    def add_available_dates(self, dates: list[DeliveryDate]):
        self._available_dates += dates

    def evaluate_date(self, date: DeliveryDate):
        self._as_evaluator_dates.append(date)

    def tutor_date(self, date: DeliveryDate):
        self._as_tutor_dates.append(date)

    def is_avaliable(self, date: str):
        label = (d.label() for d in self._available_dates)
        return date in label

    def add_substitute_date(self, date: DeliveryDate):
        self._substitute_dates.append(date)

    def add_topic(self, topic: Topic):
        if self._topics is None:
            self._topics = []
        self._topics.append(topic)

    def find_mutual_dates(self, dates: list[DeliveryDate]):
        labels = [d.label() for d in dates]
        mutual_dates = list()

        for av in self._available_dates:
            available_date_label = av.label()
            if available_date_label in labels:
                mutual_dates.append(available_date_label)

        return mutual_dates


class SinglePeriodTutor:
    """
    This class represents a tutor as a single period,
    meaning we abstract away the other periods of the tutor and consider them as a tutor
    per period.
    This way, the algorithms do not have knowledge of the other periods of that tutor.
    """

    def __init__(
        self,
        id: int,
        period_id: int,
        name: str,
        last_name: str,
        email: str,
        capacity: int = 0,
        topics=None,
    ):
        self._id = id
        self._name = name
        self._last_name = last_name
        self._is_evaluator = False
        self._capacity = capacity
        self._topics = topics
        self._email = email
        self._period_id = period_id

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

    def topics_ids(self):
        return [topic.id for topic in self._topics]
