class CategoryAlreadyExist(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 409
        super().__init__(self.message)


class CategoryNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 404
        super().__init__(self.message)


class TopicAlreadyExist(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 409
        super().__init__(self.message)


class InvalidTopicCsv(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 415
        super().__init__(message)
