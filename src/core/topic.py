class Topic:
    def __init__(self, id: int, title: str, cost: int = 0, capacity=0, category=None):
        self._id = id
        self._title = title
        self._category = category
        self._cost = cost
        self._capacity = capacity

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self):
        return self._title

    @property
    def cost(self):
        return self._cost

    @property
    def capacity(self):
        return self._capacity

    @property
    def category(self):
        return self._category
