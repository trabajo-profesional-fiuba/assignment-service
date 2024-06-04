from src.model.topic import Topic
from src.model.tutor.tutor import Tutor


class InitialStateTutor(Tutor):
    """
    Represents the initial state of a tutor.
    """

    def __init__(self, id: int, capacity: int, topics: list[Topic]) -> None:
        """
        Initializes an `InitialStateTutor` object.
        Attributes:
            id (int): The identifier of the tutor.
            capacity (int): The group capacity of the tutor.
            topics (list[Topic]): A list of topic ordered by topic id.
        """
        self._capacity = capacity
        self._topics = topics

    @property
    def capacity(self) -> int:
        """Returns the capacity of the tutor."""
        return self._capacity

    @property
    def topics(self) -> list[Topic]:
        """Returns the list of topics ordered by topic id."""
        return self._topics

    def preference_of(self, topic: Topic) -> int:
        """
        Calculates the preference_of of a given topic for the tutor.
        Args:
            topic (Topic): The topic for which the preference_of is calculated.
        Returns:
            int: The tutor's preference_of for the given topic.
        """
        return self._topics[topic.id - 1].cost

    def capacity_of(self, topic: Topic) -> int:
        """
        Retrieves the capacity of the tutor for a given topic.
        Args:
            topic (Topic): The topic for which the capacity is retrieved.
        Returns:
            int: The tutor's capacity for the given topic.
        """
        return self._topics[topic.id - 1].capacity
