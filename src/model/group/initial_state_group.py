from src.model.topic import Topic
from src.model.tutor.tutor import Tutor

class InitialStateGroup():

    def __init__(self, topics):
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
        self._topics = topics


    @property
    def topics(self):
        """
        Gets the dict of topics and its given preferences.

        Returns a dict with topics.
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


    def assign(self, tutor: Tutor, group):
        """
        Assigns a tutor to the group.
        Double-Distpatch is performed

        Args:
            tutor: The tutor to be assigned to the group.
        """
        group.assign_tutor(tutor)
        

