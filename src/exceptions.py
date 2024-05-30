class TutorNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class WeekNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DayNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HourNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
