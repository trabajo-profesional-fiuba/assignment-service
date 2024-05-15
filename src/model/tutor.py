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
