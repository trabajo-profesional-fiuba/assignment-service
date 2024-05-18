class Group:

    def __init__(self, id: str, costs: list):
        """When _ is used, that means is a private attribute"""
        self._id = id
        self._costs = costs

    @property
    def id(self):
        return self._id

    @property
    def costs(self):
        return self._costs
