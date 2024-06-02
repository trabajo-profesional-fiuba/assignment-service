from src.model.topic import Topic


class Tutor:

    def __init__(self, id ,email, name, groups=None):
        self._id = id
        self._name = name
        self._email = email
        self._groups = groups

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    
    def assign_group(self, group):
        self._groups.append(group)

