from fastapi import status


class InvalidTutorCsv(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class CsvNotLoaded(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorDuplicated(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorNotInserted(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


class PeriodDuplicated(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class InvalidPeriodId(Exception):
    def __init__(self, message):
        super().__init__()
        self._message = message

    def message(self):
        return self._message


class TutorPeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
