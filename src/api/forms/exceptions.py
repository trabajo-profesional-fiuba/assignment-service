# Internal
class AnswerNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


# External