from src.api.student.utils import StudentCsvFile
from src.api.users.schemas import UserList
from src.api.users.model import User, Role
from src.api.auth.hasher import ShaHasher
from src.api.student.exceptions import StudentDuplicated, StudentNotFound


class StudentService:

    def __init__(self, repository) -> None:
        self._repository = repository

    def _get_csv_rows(self, csv: str):
        csv_file = StudentCsvFile(csv=csv)
        return csv_file.get_info_as_rows()

    def _get_students(self, rows, hasher: ShaHasher):
        students = []
        for i in rows:
            name, last_name, student_id, email = i
            student = User(
                name=name,
                last_name=last_name,
                id=int(student_id),
                email=email,
                password=hasher.hash(str(student_id)),
                role=Role.STUDENT,
            )
            students.append(student)
        return students

    def create_students_from_string(self, csv: str, hasher: ShaHasher):
        rows = self._get_csv_rows(csv)
        students = self._get_students(rows, hasher)
        self._repository.delete_students()
        students_saved = self._repository.add_students(students)
        return UserList.model_validate(students_saved)

    def get_students_by_ids(self, ids: list[int]):
        if len(list(set(ids))) != len(list(ids)):
            raise StudentDuplicated("Query params student ids contain duplicates")

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
