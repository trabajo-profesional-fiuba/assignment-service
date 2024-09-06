from sqlalchemy.orm import Session
from sqlalchemy import exc, select, update

from src.api.students.exceptions import StudentDuplicated, StudentNotInserted
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted
from src.api.users.exceptions import UserNotFound
from src.api.users.models import User, Role


class UserRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def get_user_by_email(self, email: str):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).one_or_none()
            if not user:
                raise UserNotFound("User not found")
            session.expunge(user)

        return user

    def _add_users(self, new_users: list[User]):
        with self.Session() as session:
            session.add_all(new_users)
            session.commit()
            for user in new_users:
                session.refresh(user)
                session.expunge(user)

        return new_users

    def add_tutors(self, tutors: list[User]):
        try:
            return self._add_users(tutors)
        except exc.IntegrityError as e:
            raise TutorDuplicated("Duplicated tutor")
        except Exception:
            raise TutorNotInserted("Could not insert a student in the database")

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
                for student in students:
                    stmt = (
                        select(User)
                        .filter_by(role=Role.STUDENT)
                        .where(User.id == student.id))
                    student_db = session.execute(stmt).scalars().first()
                    if student_db is None:
                        session.add(student)
                        session.commit()
                        session.refresh(student)
                        session.expunge(student)
                        
                    else:
                        update_stmt = (
                            update(User)
                            .where(User.id == student.id)
                            .values(name=student.name, last_name=student.last_name))
                        session.execute(update_stmt)
                        session.commit()

            return students
        except Exception as e:
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
