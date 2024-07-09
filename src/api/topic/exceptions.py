class TopicPreferencesNotFound(Exception):
    def __init__(self):
        pass


class TopicCategoryDuplicated(Exception):
    def __init__(self):
        pass


class TopicCategoryNotFound(Exception):
    def __init__(self):
        pass


class TopicDuplicated(Exception):
    def __init__(self):
        pass


class StudentEmailDuplicated(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(self.email)


class TopicPreferencesDuplicated(Exception):
    def __init__(self):
        pass
