from src.model.tutor import Tutor
from src.model.utils.topic import Topic
from src.model.utils.delivery_date import DeliveryDate


class Group:

    def __init__(self, id: int, tutor=None) -> None:
        self._id = id
        self._tutor = tutor
        self._available_dates = []
        self._assigned_date = None
        self._topics = []

    def id(self) -> str:
        return self._id

    @property
    def tutor(self):
        return self._tutor

    @property
    def assigned_date(self):
        return self._assigned_date

    @property
    def available_dates(self):
        return self._available_dates

    @property
    def topics(self) -> list[Topic]:
        """
        Returns a list of topics.
        """
        return self._topics

    def add_topics(self, topics: list[Topic]):
        self._topics = topics

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
