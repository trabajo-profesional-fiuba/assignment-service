class TutorDuplicated(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorPeriodNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)


class TutorPeriodNotInserted(Exception):
    def __init__(self, message):
        super().__init__(message)
