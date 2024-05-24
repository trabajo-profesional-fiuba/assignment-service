from src.model.group.base_group import BaseGroup
from src.model.topic import Topic
from src.model.tutor import Tutor


class InitialStateGroup(BaseGroup):

    def __init__(self, id: str, topics: dict):
        """
        Initializes the class with an id and a dict of topics.

        Args:
            id: The unique identifier for the instance.
            topics: The dict of topics ordered by preference.

        Attributes:
            _topics: Stores the topics ordered by preference.
            _tutor: Initially set to None, this will hold the
            tutor assigned to the group.
        """
        super().__init__(id)
        self._topics = topics
        self._tutor = None

    @property
    def topics(self):
        """
        Gets the dict of topics and its given preferences.

        Returns a dict with topics.
        """
        return self._topics

    def cost_of(self, topic: Topic):
        """
        Calculates the cost of a given topic based on the group's preferences.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        return self.topics[topic.id]

    def assign_tutor(self, tutor: Tutor):
        """
        Assigns a tutor to the group.

        Args:
            tutor: The tutor to be assigned to the group.
        """
        self._tutor = tutor
