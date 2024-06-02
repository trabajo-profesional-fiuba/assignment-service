from src.model.tutor.tutor import Tutor


class InitialStateTutor(Tutor):
    
    def __init__(self, id, email, name, global_capacity, topics):
        super().__init__(id, email, name)
        self._topics = topics
        self._global_capacity = global_capacity

    @property
    def global_capacity(self):
        return self._global_capacity

    @property
    def topics(self):
        return self._topics
    
    def preference_of(self, topic):
        for t in self._topics:
            if topic.id == t.id:
                return t.cost

    def capacity_of(self, topic):
        for t in self._topics:
            if topic.id == t.id:
                return t.capacity
        