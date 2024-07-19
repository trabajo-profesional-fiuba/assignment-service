from sqlalchemy.orm import Session

from src.api.tutors.schemas import Tutor
from src.api.tutors.model import TutorModel
from src.api.tutors.exceptions import TutorDuplicated


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_tutors(self, tutors: list[Tutor]):
        # create session and add objects
        # Si se hace como transaccion y luego el commit, es mas optimo.
        try:
            with self.Session() as session:
                with session.begin():
                    tutors_objs = []
                    for student in tutors:
                        student_obj = TutorModel(
                            dni=student.dni,
                            name=student.name,
                            last_name=student.last_name,
                            email=student.email,
                            password=student.password,
                        )
                        tutors_objs.append(student_obj)

                    session.add_all(tutors_objs)

                # inner context calls session.commit(), if there were no exceptions
            # outer context calls session.close()
        except:
            raise TutorDuplicated("Could not insert a student in the database")