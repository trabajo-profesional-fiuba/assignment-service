from src.model.topic import Topic
from src.model.tutor.tutor import Tutor


class InitialStateGroup:

    def __init__(self, topics: list[Topic]) -> None:
        """
        Initializes the class with a list of topics.

        Args:
            topics: The list of topics.

        Attributes:
            _topics: Stores the topics.
        """
        self._topics = topics

    @property
    def topics(self) -> list[Topic]:
        """
        Returns a list of topics.
        """
        return self._topics

    def preference_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        return self._topics[topic.id - 1].cost
