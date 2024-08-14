from fastapi import status
from fastapi.exceptions import HTTPException


class TutorDuplicated(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorNotInserted(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class PeriodDuplicated(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorPeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


# External
class InvalidPeriod(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)
