from src.api.student.schemas import Student
from src.api.student.model import StudentModel
from src.config.database import Database
from src.api.student.exceptions import StudentDuplicated


class StudentRepository:

    def __init__(self, db: Database):
        self._db = db

    def add_students(self, students: list[Student]):
        # create session and add objects
        # Si se hace como transaccion y luego el commit, es mas optimo.
        try:
            with self._db.get_session() as session:
                with session.begin():
                    students_objs = []
                    for student in students:
                        student_obj = StudentModel(
                            id=student.id,
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
