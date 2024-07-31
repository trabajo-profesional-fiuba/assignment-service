from fastapi import status


class StudentNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


class TopicNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


class DuplicatedAnswer(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_409_CONFLICT


class GroupIdNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
