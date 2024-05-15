class Topic:

    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id
