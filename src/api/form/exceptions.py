class UidDuplicated(Exception):
    def __init__(self, name: str):
        self.name = name
        self.status_code = 409
        super().__init__(self.name)


class TopicNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 409
        super().__init__(self.message)
