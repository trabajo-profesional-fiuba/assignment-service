from pydantic import BaseModel


class StudentBase(BaseModel):
    uid: int
    name: str
    last_name: str
    email: str
    password: str
