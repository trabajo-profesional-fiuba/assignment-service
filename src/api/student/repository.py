from sqlalchemy.orm import Session

from src.api.users.schemas import UserResponse
from src.api.users.model import User, Role


class StudentRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def get_students(self):
        with self.Session() as session:
            students_found = []
            students = session.query(User).filter(User.role == Role.STUDENT).all()
            for student in students:
                students_found.append(UserResponse.model_validate(student))

            return students_found

    def get_students_by_ids(self, ids: list[int]):
        with self.Session() as session:
            students_found = []
            students = session.query(User).filter(User.id.in_(ids)).all()
            for student in students:
                students_found.append(UserResponse.model_validate(student))

            return students_found
