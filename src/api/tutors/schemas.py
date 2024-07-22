from pydantic import BaseModel


class Tutor(BaseModel):
    dni: int
    name: str
    last_name: str
    email: str
    password: str
