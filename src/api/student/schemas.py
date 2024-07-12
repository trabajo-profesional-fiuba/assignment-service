from pydantic import BaseModel

class Student(BaseModel):
    id: str
    name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True