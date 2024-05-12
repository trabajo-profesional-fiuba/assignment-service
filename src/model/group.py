class Group:

    def __init__(self, id: str, weights: list):
        """ When _ is used, that means is a private attribute"""
        self._id = id
        self._weights = weights

    @property
    def id(self):
        return self._id

    @property
    def weights(self):
        return self._weights