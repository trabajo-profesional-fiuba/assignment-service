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

    def _add_users(self, new_users: list[UserResponse], role: Role):
        with self.Session() as session:
            with session.begin():
                user_objs = []
                for user in new_users:
                    user_obj = User(
                        id=user.id,
                        name=user.name,
                        last_name=user.last_name,
                        email=user.email,
                        password=user.password,
                        rol=role,
                    )
                    user_objs.append(user_obj)
                session.add_all(user_objs)
                return user_objs

    def add_tutors(self, tutors: list[UserResponse]):
        # create session and add objects
        try:
            return self._add_users(tutors, Role.TUTOR)
        except exc.IntegrityError as e:
            raise TutorDuplicated("Duplicated tutor")
        except:
            raise TutorNotInserted("Could not insert a student in the database")

    def add_students(self, students: list[UserResponse]):
        # create session and add objects
        try:
            return self._add_users(students, Role.STUDENT)
        except exc.IntegrityError as e:
            raise StudentDuplicated("Student duplicated")
        except:
            raise StudentNotInserted("Could not insert a student in the database")
