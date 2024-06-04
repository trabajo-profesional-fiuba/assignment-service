from src.model.topic import Topic


class Tutor:

    def __init__(self, id: int, email: str, name: str, groups=None, state=None) -> None:
        self._id = id
        self._name = name
        self._email = email
        self._groups = groups
        self._state = state

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def topics(self) -> list[Topic]:
        return self._state.topics

    def assign_group(self, group) -> None:
        self._groups.append(group)

    def preference_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        return self._state.preference_of(topic)

    def capacity_of(self, topic: Topic) -> int:
        """
        Calculates the capacity of a given topic.

        Args:
            - topic: The topic for which the capacity is calculated.

        Returns the group's capacity for the given topic.
        """
        return self._state.capacity_of(topic)

    def capacity(self) -> int:
        """Returns the capacity of the tutor."""
        return self._state.capacity

    def assign_date(self, date: str) -> None:
        self._state.assign_date(date)

    def assigned_dates(self) -> str:
        return self._state.assigned_dates()
