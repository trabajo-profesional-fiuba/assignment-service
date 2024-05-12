class Tutor:

    def __init__(self, id: str, team_capacity: int, topics_capacities: list, topics_weights: list):
        self._id = id
        self._capacity = team_capacity
        self._topics_capacities = topics_capacities
        self._topics_weights = topics_weights

    @property
    def id(self):
        return self._id
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def topics_capacities(self):
        return self._topics_capacities

    @property
    def topics_weights(self):
        return self._topics_weights