from sqlalchemy.orm import Session
from sqlalchemy import exc, select

from src.api.exceptions import Duplicated
from src.api.students.exceptions import StudentDuplicated, StudentNotInserted
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted
from src.api.users.exceptions import UserNotFound
from src.api.users.models import User, Role


class UserRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _add_users(self, new_users: list[User]):
        with self.Session() as session:
            session.add_all(new_users)
            session.commit()
            for user in new_users:
                session.refresh(user)
                session.expunge(user)

        return new_users

    def add_user(self, new_user: User):
        try:
            with self.Session() as session:
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
                session.expunge(new_user)
            return new_user
        except exc.IntegrityError:
            raise Duplicated("User duplicated")

    def add_tutors(self, tutors: list[User]):
        try:
            return self._add_users(tutors)
        except exc.IntegrityError:
            raise TutorDuplicated("Duplicated tutor")
        except Exception:
            raise TutorNotInserted("Could not insert a tutor in the database")

    def add_students(self, students: list[User]):
        try:
            return self._add_users(students)
        except exc.IntegrityError:
            raise StudentDuplicated("Student duplicated")
        except Exception:
            raise StudentNotInserted("Could not insert a student in the database")

    def upsert_students(self, students: list[User]):
        try:
            with self.Session() as session:
                student_ids = [student.id for student in students]
                # Select all existing students with matching IDs
                stmt = (
                    select(User)
                    .filter_by(role=Role.STUDENT)
                    .where(User.id.in_(student_ids))
                )
                existing_students = session.execute(stmt).scalars().all()
                existing_ids = {student.id for student in existing_students}

                # Split into new and existing students
                new_students = [
                    student for student in students if student.id not in existing_ids
                ]
                update_students = [
                    student for student in students if student.id in existing_ids
                ]

                # Bulk insert new students
                if new_students:
                    session.bulk_save_objects(new_students)
                    session.commit()

                # Bulk update existing students
                if update_students:
                    # Add relevant fields
                    update_mappings = [
                        {
                            "id": student.id,
                            "name": student.name,
                            "last_name": student.last_name,
                            "email": student.email,
                        }
                        for student in update_students
                    ]
                    session.bulk_update_mappings(User, update_mappings)
                    session.commit()

                return students
        except Exception:
            raise StudentNotInserted("Could not insert a student in the database")

    def delete_students(self):
        with self.Session() as session:
            session.query(User).filter(User.role == Role.STUDENT).delete()
            session.commit()

    def delete_tutors(self):
        with self.Session() as session:
            session.query(User).filter(User.role == Role.TUTOR).delete()
            session.commit()

    def get_tutors(self):
        with self.Session() as session:
            tutors = session.query(User).filter(User.role == Role.TUTOR).all()
            session.expunge_all()
        return tutors

    def get_tutor_by_id(self, tutor_id: int):
        with self.Session() as session:
            tutor = (
                session.query(User)
                .select_from(User)
                .where(User.id == tutor_id)
                .one_or_none()
            )

        return tutor

    def get_user_by_email(self, email: str):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).one_or_none()
            if not user:
                raise UserNotFound("User not found")
            session.expunge(user)

        return user

    def get_user_by_id(self, user_id: int):
        with self.Session() as session:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if not user:
                raise UserNotFound("User not found")
            session.expunge(user)

        return user
