from src.model.topic import Topic
from typing import list


class InitialStateGroup:

    def __init__(self, topics):
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

    def preference_of(self, topic: Topic):
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        for t in self._topics:
            if topic.id == t.id:
                return t.cost
