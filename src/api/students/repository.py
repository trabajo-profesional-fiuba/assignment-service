from sqlalchemy import exc, select, update
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.orm import Session
from src.api.groups.models import Group
from src.api.topics.models import Topic
from src.api.tutors.models import TutorPeriod
from src.api.periods.models import Period
from src.api.users.models import User, Role
from src.api.periods.exceptions import PeriodDuplicated
from src.api.students.exceptions import StudentNotFound, StudentPeriodNotInserted
from src.api.students.models import StudentPeriod


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

    def add_student_period(self, student_period: StudentPeriod) -> StudentPeriod:
        try:
            with self.Session() as session:
                session.add(student_period)
                session.commit()

            return student_period
        except exc.IntegrityError:
            raise PeriodDuplicated(message="Period can't be assigned to student")

    def get_period_by_student_id(self, student_id: int) -> Period:
        with self.Session() as session:
            student_period = (
                session.query(StudentPeriod)
                .filter(StudentPeriod.student_id == student_id)
                .first()
            )
            if student_period:
                return student_period
            raise StudentNotFound("The student id is not registered")

    def add_student_periods(
        self, student_periods: list[StudentPeriod]
    ) -> list[StudentPeriod]:
        try:
            with self.Session() as session:
                session.add_all(student_periods)
                session.commit()
                session.expunge_all()

            return student_periods
        except exc.IntegrityError as e:
            raise PeriodDuplicated(message=f"{e}")

    def upsert_student_periods(self, student_periods: list[StudentPeriod]):
        try:
            with self.Session() as session:
                student_ids = {sp.student_id for sp in student_periods}

                # Select existing student periods
                stmt = select(StudentPeriod).where(
                    StudentPeriod.student_id.in_(student_ids)
                )
                existing_student_periods = session.execute(stmt).scalars().all()
                existing_keys = {sp.student_id for sp in existing_student_periods}

                # Classify into new and existing student periods
                new_student_periods = [
                    sp for sp in student_periods if sp.student_id not in existing_keys
                ]
                update_student_periods = [
                    sp for sp in student_periods if sp.student_id in existing_keys
                ]

                # Bulk insert new student periods
                if new_student_periods:
                    session.bulk_save_objects(new_student_periods)
                    session.commit()

                # Bulk update existing student periods
                if update_student_periods:
                    for sp in update_student_periods:
                        session.merge(sp)
                    session.commit()

                return student_periods
        except Exception as e:
            raise StudentPeriodNotInserted(
                "Could not insert student periods in the database"
            )
