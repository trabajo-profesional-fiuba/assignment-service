class InvalidTutorCsv(Exception):
    def __init__(self, message):
        super().__init__(message)


class CsvNotLoaded(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)
