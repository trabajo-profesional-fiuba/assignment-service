class InvalidStudentCsv(Exception):
    def __init__(self, message):
        super().__init__(message)
class CsvNotLoaded(Exception):
    def __init__(self, message):
        super().__init__(message)
class StudentDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)
