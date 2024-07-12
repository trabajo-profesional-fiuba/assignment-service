from src.api.student.utils import StudentCsvFile
from src.api.student.schemas import Student
from src.api.auth.hasher import ShaHasher


class StudentService:

    def __init__(self, repository: None) -> None:
        self._repository = repository

    def create_students_from_string(self, csv: str, hasher: ShaHasher):
        students = []
        csv_file = StudentCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        for i in rows:
            student = Student(
                name=i[0],
                last_name=i[1],
                id=str(i[2]),
                email=i[3],
                password=hasher.hash(str(i[2])),
            )

            students.append(student)

        return students
