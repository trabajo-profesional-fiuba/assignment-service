from fastapi import status


class InvalidTopicCsv(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(message)


class TopicAlreadyExist(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(self.message)


class InvalidMediaType(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        super().__init__(message)
