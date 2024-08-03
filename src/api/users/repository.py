from sqlalchemy.orm import Session
from sqlalchemy import exc


from src.api.users.model import User, Role
from src.api.users.schemas import UserResponse
from src.api.users.exceptions import UserNotFound

from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted
from src.api.student.exceptions import StudentDuplicated, StudentNotInserted


class UserRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def get_user_by_email(self, email: str):
        with self.Session() as session:
            user = session.query(User).filter(User.email == email).one_or_none()
            if not user:
                raise UserNotFound("User not found")

            # FIXME - Separar en schema
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
        # create session and add objects
        try:
            return self._add_users(tutors)
        except exc.IntegrityError as e:
            print(str(e))
            raise TutorDuplicated("Duplicated tutor")
        except:
            raise TutorNotInserted("Could not insert a student in the database")

    def add_students(self, students: list[User]):
        # create session and add objects
        try:
            return self._add_users(students)
        except exc.IntegrityError as e:
            raise StudentDuplicated("Student duplicated")
        except:
            raise StudentNotInserted("Could not insert a student in the database")
