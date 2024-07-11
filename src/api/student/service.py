from src.api.student.utils import StudentCsvFile
class StudentService:

    def __init__(self,repository: None) -> None:
        self._repository = repository

    
    def create_students_from_string(self, csv: str):
        csv_file = StudentCsvFile(csv=csv)
        return csv_file