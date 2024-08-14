# Internal
class StudentNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class TopicNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class AnswerNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

# External


