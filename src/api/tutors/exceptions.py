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
