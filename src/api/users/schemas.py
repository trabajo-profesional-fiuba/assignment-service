from pydantic import BaseModel, ConfigDict, RootModel
from typing import List


class UserResponse(BaseModel):
    """Schema de respuesta representando un usuario"""

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
    """Lista de respuestas de usuarios"""

    root: List[UserResponse]

    def __iter__(self):
        return iter(self.root)
