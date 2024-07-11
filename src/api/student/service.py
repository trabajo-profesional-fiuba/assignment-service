from io import StringIO
import pandas as pd

class StudentService:

    def __init__(self,repository: None) -> None:
        self._repository = repository

    
    def create_students_from_string(self, csv: str):
        file = StringIO(csv)
        df = pd.read_csv(file)
        return df