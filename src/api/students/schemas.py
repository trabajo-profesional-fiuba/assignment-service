from pydantic import BaseModel
from typing import List
from src.api.users.schemas import UserResponse

class PersonalInformation(BaseModel):
    id: int
    form_answered: bool
    group_id: int
    tutor: str
    topic: str
    teammates: List[str]
    period_id: str

class StudentRequest(UserResponse):
    id: int
    name: str
    last_name: str
    email: str