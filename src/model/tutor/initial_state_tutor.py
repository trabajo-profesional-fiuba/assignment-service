from src.model.topic import Topic
from src.model.tutor.base_tutor import BaseTutor
from typing import Dict

class InitialStateTutor(BaseTutor):
    """
    Represents the initial state of a tutor.

    Attributes:
        id (str): The identifier of the tutor.
        capacity (int): The capacity of the tutor.
        topics (dict): A dictionary containing costs and capacities for each topic.
    """

    def __init__(self, id: str, capacity: int, topics: Dict[str, List[int]]) -> None:
        """
        Initializes an InitialStateTutor object.

        Args:
            id (str): The identifier of the tutor.
            capacity (int): The capacity of the tutor.
            topics (dict): A dictionary containing costs and capacities for each topic.
        """
        super().__init__(id)
        self._capacity = capacity
        self._topics = topics

    @property
    def capacity(self) -> int:
        """Returns the capacity of the tutor."""
        return self._capacity

    @property
    def topics(self) -> Dict[str, List[int]]:
        """Returns the topics dictionary containing costs and capacities."""
        return self._topics

    def cost_of(self, topic: Topic) -> int:
        """
        Calculates the cost of a given topic for the tutor.

        Args:
            topic (Topic): The topic for which the cost is calculated.

        Returns:
            int: The tutor's cost for the given topic.
        """
        id = int(topic.id[1:])
        return self._topics["costs"][id - 1]

    def capacity_of(self, topic: Topic) -> int:
        """
        Retrieves the capacity of the tutor for a given topic.

        Args:
            topic (Topic): The topic for which the capacity is retrieved.

        Returns:
            int: The tutor's capacity for the given topic.
        """
        id = int(topic.id[1:])
        return self._topics["capacities"][id - 1]
