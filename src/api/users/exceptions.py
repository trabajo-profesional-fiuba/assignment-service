from fastapi import status
from fastapi.exceptions import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidCredentials(UserNotFound):
    def __init__(self, message: str):
        super().__init__(message)
