class BaseGroup:

    def __init__(self, id: str):
        """When _ is used, that means is a private attribute"""
        self._id = id

    @property
    def id(self):
        return self._id
