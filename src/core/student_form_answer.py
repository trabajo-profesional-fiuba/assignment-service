class StudentFormAnswer:
    def __init__(self, id: int, answer_id: str, topics: list = None):
        self._id = id
        self._answer_id = answer_id
        self._topics = topics if topics is not None else []

    @property
    def id(self):
        return self._id

    @property
    def answer_id(self):
        return self._answer_id

    @property
    def topics(self):
        return self._topics
