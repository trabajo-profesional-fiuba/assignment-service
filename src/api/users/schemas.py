from typing import List
from pydantic import BaseModel, ConfigDict, RootModel


class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

    def __eq__(self, other):
        if not isinstance(other, UserResponse):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.last_name == other.last_name
            and self.email == other.email
            and self.password == other.password
        )


class UserList(RootModel):
    root: List[UserResponse]

    def __iter__(self):
        return iter(self.root)


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