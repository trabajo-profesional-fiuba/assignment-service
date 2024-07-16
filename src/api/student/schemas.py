from pydantic import BaseModel

class Student(BaseModel):
    uid: int
    name: str
    last_name: str
    email: str
    password: str