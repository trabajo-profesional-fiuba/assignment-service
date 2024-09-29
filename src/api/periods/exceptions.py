from fastapi import status
from fastapi.exceptions import HTTPException


class PeriodDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)


class PeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


# External
class InvalidPeriod(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)
