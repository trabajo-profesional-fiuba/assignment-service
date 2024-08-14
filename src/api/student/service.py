from src.api.student.utils import StudentCsvFile
from src.api.users.schemas import UserList
from src.api.users.model import User, Role
from src.api.auth.hasher import ShaHasher
from src.api.student.exceptions import (
    StudentDuplicated,
    StudentNotFound,
    StudentNotInserted,
)
from src.api.exceptions import Duplicated, EntityNotFound, EntityNotInserted, InvalidCsv


class StudentService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def create_students_from_string(self, csv: str, hasher: ShaHasher):
        try:
            students_db = []
            csv_file = StudentCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            for i in rows:
                name, last_name, id, email = i
                student = User(
                    name=name,
                    last_name=last_name,
                    id=int(id),
                    email=email,
                    password=hasher.hash(str(id)),
                    role=Role.STUDENT,
                )
                students_db.append(student)
            students_saved = self._repository.add_students(students_db)
            students = UserList.model_validate(students_saved)
            return students
        except (InvalidCsv) as e:
            raise e
        except (StudentDuplicated) as e:
            raise Duplicated(str(e))
        except StudentNotInserted as e:
            raise EntityNotInserted(str(e))


    def get_students_by_ids(self, ids: list[int]):

        try:
            if len(list(set(ids))) != len(list(ids)):
                raise StudentDuplicated("Query params udis contain duplicates")

            if len(ids) > 0:
                students_db = self._repository.get_students_by_ids(ids)
            else:
                students_db = self._repository.get_students()

            students = UserList.model_validate(students_db)
            udis_from_db = [student.id for student in students]
            for id in ids:
                if id not in udis_from_db:
                    raise StudentNotFound(f"{id}, is not registered in the database")

            return students
        except (StudentNotFound) as e:
            raise EntityNotFound(str(e))
        except (StudentDuplicated) as e:
            raise Duplicated(str(e))