from .group import Group


class InitialStateGroup(Group):

    def __init__(self, id: str, topics: list):
        """When _ is used, that means is a private attribute"""
        super().__init__(id)
        self._topics = topics
        self._tutor = None

    @property
    def topics(self):
        "Returns the preferable topics ."
        return self._topics

    def cost_of(self, topic_id: int):
        "Returns the cost of a topic."
        return self.topics[topic_id]

    def assign_tutor(self, tutor_id: str):
        "Sets the tutor_id of the group."
        self._tutor = tutor_id
