from src.api.student.utils import StudentCsvFile
from src.api.student.schemas import StudentBase
from src.api.student.repository import StudentRepository
from src.api.auth.hasher import ShaHasher
from src.api.student.exceptions import InvalidStudentCsv, StudentDuplicated


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

            print(students)
            self._repository.add_students(students)

            return students
        except (InvalidStudentCsv, StudentDuplicated) as e:
            raise e
