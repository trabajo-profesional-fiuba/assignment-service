# Internal
class TopicNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class CategoryNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
