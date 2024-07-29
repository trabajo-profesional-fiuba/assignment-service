class GroupTopicPreferences:
    def __init__(self, id: int, topics=[], students=[]):
        self._id = id
        self._topics = topics
        self._students = students

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



