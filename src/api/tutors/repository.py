from sqlalchemy.orm import Session
from sqlalchemy import exc

from src.api.tutors.schemas import Tutor
from src.api.users.model import User, Role
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_tutors(self, tutors: list[Tutor]):
        # create session and add objects
        try:
            with self.Session() as session:
                with session.begin():
                    tutors_objs = []
                    for tutor in tutors:
                        tutor_obj = User(
                            id=tutor.id,
                            name=tutor.name,
                            last_name=tutor.last_name,
                            email=tutor.email,
                            password=tutor.password,
                            role = Role.TUTOR
                        )
                        tutors_objs.append(tutor_obj)

                    session.add_all(tutors_objs)

                # inner context calls session.commit(), if there were no exceptions
            # outer context calls session.close()
        except exc.IntegrityError as error:
            raise TutorDuplicated("Duplicated tutor")
        except:
            raise TutorNotInserted("Could not insert a student in the database")
