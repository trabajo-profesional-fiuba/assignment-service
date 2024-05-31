from typing import List
from src.model.group.base_group import BaseGroup
from src.model.topic import Topic


class InitialStateGroup(BaseGroup):

    def __init__(self, id: str, topics: List[Topic]) -> None:
        """
        Initializes the class with an id and a list of topics.

        Args:
            id: The unique identifier for the instance.
            topics: The list of topics.

        Attributes:
            _topics: Stores the topics.
            _tutor: Initially set to None, this will hold the
            tutor assigned to the group.
        """
        super().__init__(id)
        self._topics = topics

    @property
    def topics(self) -> List[Topic]:
        """
        Returns a list of topics.
        """
        return self._topics

    def cost_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.

        The cost is determined by retrieving the cost value
        associated with the topic's identifier from the group's
        list of topics.
        """
        id = int(topic.id[1:])
        return self._topics[id - 1]
