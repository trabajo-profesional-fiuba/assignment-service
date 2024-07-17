class TopicPreferencesNotFound(Exception):
    def __init__(self):
        pass


class CategoryDuplicated(Exception):
    def __init__(self):
        pass


class TopicCategoryNotFound(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 404
        super().__init__(self.message)


class TopicDuplicated(Exception):
    def __init__(self):
        pass


class UidDuplicated(Exception):
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


class InsertTopicException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 409
        super().__init__(self.message)