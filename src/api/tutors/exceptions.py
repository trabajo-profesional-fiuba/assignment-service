from fastapi import status
from fastapi.exceptions import HTTPException


class TutorDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class PeriodDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorPeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorPeriodNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)


class PeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


# External
class InvalidPeriod(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)
