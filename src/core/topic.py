class Topic:
    def __init__(self, id: int, name: str, capacity, category, cost=0):
        self._id = id
        self._name = name
        self._category = category
        self._cost = cost
        self._capacity = capacity

    @property
    def id(self) -> str:
        """
        Get the identifier of the topic.

        Returns:
            str: The identifier of the topic.
        """
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    @property
    def capacity(self):
        return self._capacity

    @property
    def category(self):
        return self._category
