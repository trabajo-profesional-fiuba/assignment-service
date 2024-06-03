class Topic:

    def __init__(self, id, title, cost, capacity=0):
        self._id = id
        self._title = title
        self._cost = cost
        self._capacity = capacity

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def cost(self):
        return self._cost

    @property
    def capacity(self):
        return self._capacity
