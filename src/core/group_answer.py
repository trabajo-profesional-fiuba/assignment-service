class GroupFormAnswer:
    def __init__(self, id: str):
        self._id = id
        self._topics = []
        self._students = []

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
    
    def add_topics(self, topics):
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