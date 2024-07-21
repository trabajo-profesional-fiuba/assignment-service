from sqlalchemy.orm import Session

from src.api.student.schemas import Student
from src.api.student.model import Student
from src.api.student.exceptions import StudentDuplicated


class StudentRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_students(self, students: list[Student]):
        # create session and add objects
        # Si se hace como transaccion y luego el commit, es mas optimo.
        try:
            with self.Session() as session:
                with session.begin():
                    students_objs = []
                    for student in students:
                        student_obj = Student(
                            uid=student.uid,
                            name=student.name,
                            last_name=student.last_name,
                            email=student.email,
                            password=student.password,
                        )
                        students_objs.append(student_obj)

                    session.add_all(students_objs)

                # inner context calls session.commit(), if there were no exceptions
            # outer context calls session.close()
        except:
            raise StudentDuplicated("Could not insert a student in the database")
