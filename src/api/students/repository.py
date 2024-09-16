from sqlalchemy import select
from sqlalchemy.orm import Session
from src.api.groups.models import Group
from src.api.topics.models import Topic
from src.api.tutors.models import TutorPeriod
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

    def get_student_info(self, id: int):
        with self.Session() as session:
            student_info = (
                session.query(
                    User.id.label("user_id"),
                    Group.id.label("group_id"),
                    Topic.name.label("topic_name"),
                    TutorPeriod.tutor_id.label("tutor_id"),
                )
                .select_from(User)
                .join(Group.students)
                .join(Group.topic)
                .join(Group.tutor_period)
                .where(User.id == id)
                .one_or_none()
            )

        return student_info

    def get_teammates(self, id: int, group_id: int):
        with self.Session() as session:
            teammates = (
                session.query(User)
                .select_from(User)
                .join(Group.students)
                .where(User.id != id)
                .where(Group.id == group_id)
            )

        return teammates
