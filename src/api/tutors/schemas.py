from pydantic import BaseModel


class Tutor(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    password: str
