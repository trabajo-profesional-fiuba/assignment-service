# Internal
class GroupNotInserted(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message
