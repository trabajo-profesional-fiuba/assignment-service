from fastapi import status


class InvalidTopicCsv(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_400_BAD_REQUEST


class TopicAlreadyExist(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_409_CONFLICT


class InvalidMediaType(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
