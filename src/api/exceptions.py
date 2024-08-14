from fastapi import status
from fastapi.exceptions import HTTPException

"""
In our application, we distinguish between internal and external exceptions to streamline error handling and response management.

Internal Exceptions: These exceptions are used within the system's runtime environment.
They are primarily employed for decision-making and controlling the flow of the application.
Internal exceptions typically represent issues or conditions that arise during the execution of the system's logic and are not directly exposed to the end users.

External Exceptions: These exceptions are designed to be communicated as responses to client requests.
They are often raised by services or controllers to signal specific error conditions that affect the client's interaction with the application.
External exceptions are associated with HTTP status codes and include messages that provide context about the error.
This distinction allows the application to respond to clients with meaningful and actionable error information.

By separating internal and external exceptions, 
we ensure that internal system issues are handled discreetly while providing clear and consistent error responses to clients.
This approach enhances both the robustness of the system and the clarity of communication with users.

"""
class EntityNotFound(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)
    
class EntityNotInserted(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_400_BAD_REQUEST)

class Duplicated(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_409_CONFLICT)

class ServerError(HTTPException):
    def __init__(self, message: str):
        super().__init__(detail=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)