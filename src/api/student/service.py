from src.api.student.utils import StudentCsvFile
from src.api.student.schemas import StudentBase
from src.api.student.repository import StudentRepository
from src.api.auth.hasher import ShaHasher
from src.api.student.exceptions import (
    InvalidStudentCsv,
    StudentDuplicated,
    StudentNotFound,
)


class StudentService:

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    def create_students_from_string(self, csv: str, hasher: ShaHasher):
        try:
            students = []
            csv_file = StudentCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            for i in rows:
                name, last_name, uid, email = i
                student = StudentBase(
                    name=name,
                    last_name=last_name,
                    uid=int(uid),
                    email=email,
                    password=hasher.hash(str(uid)),
                )
                students.append(student)
            self._repository.add_students(students)

            return students
        except (InvalidStudentCsv, StudentDuplicated) as e:
            raise e

    def get_students_by_ids(self, uids: list[int]):

        if len(list(set(uids))) != len(list(uids)):
            raise StudentDuplicated("Query params udis contain duplicates")

        students = self._repository.get_students_by_ids(uids)
        udis_from_db = [student.uid for student in students]
        for uid in uids:
            if uid not in udis_from_db:
                raise StudentNotFound(f"{uid}, is not registered in the database")

        return students
