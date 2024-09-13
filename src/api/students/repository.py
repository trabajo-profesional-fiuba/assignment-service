from sqlalchemy.orm import Session
from src.api.users.models import User, Role


class StudentRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def get_students(self):
        with self.Session() as session:
            students = session.query(User).filter(User.role == Role.STUDENT).all()
            for student in students:
                session.expunge(student)

        return students

    def get_students_by_ids(self, ids: list[int]):
        with self.Session() as session:
            students = (
                session.query(User)
                .filter(User.id.in_(ids))
                .filter(User.role == Role.STUDENT)
                .all()
            )
            for student in students:
                session.expunge(student)

        return students
