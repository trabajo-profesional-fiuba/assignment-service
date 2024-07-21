class StudentNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 404
        super().__init__(self.message)
