from src.model.topic import Topic

class Tutor:

    def __init__(self, id: str, capacity: int, topics: dict):
        self._id = id
        self._capacity = capacity
        self._topics = topics

    @property
    def id(self):
        return self._id

    @property
    def capacity(self):
        return self._capacity

    @property
    def topics(self):
        return self._topics
    
    def cost_of(self, topic: Topic):
        id = int(topic.id[1:])
        return self._topics["costs"][id - 1]
    
    def capacity_of(self, topic: Topic):
        id = int(topic.id[1:])
        return self._topics["capacities"][id - 1]
