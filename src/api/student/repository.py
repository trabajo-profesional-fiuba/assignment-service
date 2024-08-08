from sqlalchemy.orm import Session
from src.api.student.model import Group
from src.api.users.model import User, Role


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
            students = session.query(User).filter(User.id.in_(ids)).all()
            for student in students:
                session.expunge(student)

        return students

    def add_group(self, ids, period_id, topic_id):
        with self.Session() as session:
            group = Group(tutor_period_id=period_id, topic_id=topic_id)
            students = session.query(User).filter(User.id.in_(ids)).all()
            group.students = students
            session.add(group)
            session.commit()
            session.refresh(group)
            session.expunge(group)
        
        return group

