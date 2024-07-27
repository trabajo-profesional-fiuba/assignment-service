from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    password: str

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
