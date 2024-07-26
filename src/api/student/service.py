from src.api.student.utils import StudentCsvFile
from src.api.student.schemas import StudentBase
from src.api.student.repository import StudentRepository
from src.api.auth.hasher import ShaHasher
from src.api.student.exceptions import InvalidStudentCsv, StudentDuplicated, StudentNotFound


class StudentService:

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    def create_students_from_string(self, csv: str, hasher: ShaHasher):
        try:
            students = []
            csv_file = StudentCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            for i in rows:
                name, last_name, id, email = i
                student = StudentBase(
                    name=name,
                    last_name=last_name,
                    id=int(id),
                    email=email,
                    password=hasher.hash(str(id)),
                )
                students.append(student)
            self._repository.add_students(students)

            return students
        except (InvalidStudentCsv, StudentDuplicated) as e:
            raise e
    
    def get_students_by_ids(self, ids: list[int]):

        if len(list(set(ids))) != len(list(ids)):
            raise StudentDuplicated("Query params udis contain duplicates")

        students = self._repository.get_students_by_ids(ids)
        udis_from_db = [student.id for student in students]
        for id in ids:
            if id not in udis_from_db:
                raise StudentNotFound(f"{id}, is not registered in the database")

        return students