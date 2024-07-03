class TopicPreferencesDuplicated(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class StudentNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TopicCategoryDuplicated(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
