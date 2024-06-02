from src.model.group.base_group import BaseGroup
from src.model.topic import Topic
from src.model.tutor.tutor import Tutor


class InitialStateGroup(BaseGroup):

    def __init__(self, id: str, topics):
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
        Calculates the cost of a given topic.

        Args:
            - topic: The topic for which the cost is calculated.

        Returns the group's cost for the given topic.
        """
        id = int(topic.id[1:])
        return self._topics[id - 1]

    def assign_tutor(self, tutor: Tutor):
        """
        Assigns a tutor to the group.

        Args:
            tutor: The tutor to be assigned to the group.
        """
        self._tutor = tutor
