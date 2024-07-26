class InvalidStudentCsv(Exception):
    def __init__(self, message):
        super().__init__(message)

    def status_code(self):
        return 400


class CsvNotLoaded(Exception):
    def __init__(self, message):
        super().__init__(message)


class StudentDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)
    
    def status_code(self):
        return 400

class StudentNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

class StudentNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)
        