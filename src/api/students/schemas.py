from pydantic import BaseModel
from typing import List

from src.api.users.schemas import UserResponse


class PersonalInformation(BaseModel):
    """Schema para modelar la informacion personal de un estudiante"""

    id: int
    group_id: int
    group_number: int
    form_answered: bool
    tutor: str
    topic: str
    teammates: List[str]
    period_id: str


class StudentRequest(UserResponse):
    """Schema para modelar un estudiante"""

    ...
