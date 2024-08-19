# Internal
class StudentDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)


class StudentNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class StudentNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)
