from fastapi import status
from fastapi.exceptions import HTTPException




# External
class InvalidDate(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)
