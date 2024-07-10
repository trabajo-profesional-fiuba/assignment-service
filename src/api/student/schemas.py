from pydantic import BaseModel

class Student(BaseModel):
    name: str
    last_name: str
    email: str
    student_number: str



class StudentResponse(Student):
    id: int