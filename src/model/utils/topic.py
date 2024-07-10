class Topic:
    def __init__(self, id: int, title: str, cost: int, capacity=0, categories=[]):
        self._id = id
        self._title = title
        self._categories = categories
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
    def title(self):
        return self._title

    @property
    def cost(self):
        return self._cost

    @property
    def capacity(self):
        return self._capacity
    
    @property
    def categories(self):
        return self._categories
    
    def add_category(self, category):
        self._categories.append(category)
