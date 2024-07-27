from fastapi import status


class UserNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_401_UNAUTHORIZED


class InvalidCredentials(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_401_UNAUTHORIZED
