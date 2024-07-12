from src.api.student.utils import StudentCsvFile
from src.api.student.schemas import StudentResponse
from src.api.auth.hasher import SHA1Hasher


class StudentService:

    def __init__(self, repository: None) -> None:
        self._repository = repository

    def create_students_from_string(self, csv: str, hasher: SHA1Hasher):
        students = []
        csv_file = StudentCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        for i in rows:
            student = StudentResponse(
                name=i[0],
                last_name=i[1],
                student_number=str(i[2]),
                email=i[3],
                password=hasher.hash(str(i[2])),
                id=1,
            )

            students.append(student)

        return students
