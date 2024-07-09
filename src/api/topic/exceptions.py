class TopicPreferencesNotFound(Exception):
    def __init__(self):
        pass


class TopicCategoryDuplicated(Exception):
    def __init__(self):
        pass


class TopicCategoryNotFound(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(self.name)


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


class TopicNotFound(Exception):
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        super().__init__(self.name, self.category)
