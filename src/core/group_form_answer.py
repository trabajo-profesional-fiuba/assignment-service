class GroupFormAnswer:
    def __init__(self, id: str, topics: list = None, students: list = None):
        self._id = id
        # This must be done this way because python violates the principle of
        # Least Astonishment making args mutable, so if we change the = None to
        # a = list(), all the intances will shared the same list()
        self._topics = topics if topics is not None else []
        self._students = students if students is not None else []

    @property
    def id(self):
        return self._id

    @property
    def topics(self):
        return self._topics

    @property
    def students(self):
        return self._students

    def add_student(self, student):
        self._students.append(student)

    def add_students(self, students):
        self._students.extend(students)

    def add_topics(self, topics: list):
        names = [topic.name for topic in self._topics]
        for topic in topics:
            if topic.name not in names:
                self._topics.append(topic)

    def get_topic_names(self):
        names = [topic.name for topic in self._topics]
        return names

    def get_topic_ids(self):
        ids = [topic.id for topic in self._topics]
        return ids
