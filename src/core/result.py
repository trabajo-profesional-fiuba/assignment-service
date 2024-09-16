class AssignmentResult:

    def __init__(self, results, substitutes=None) -> None:
        self._results = results
        self._substitutes = substitutes

    def get_results(self):
        return self._results

    def get_substitutes(self):
        return self._substitutes


class GroupTutorAssigmentResult:
    """Represents the assigment result"""

    def __init__(self, id, tutor, topic) -> None:
        self.id = id
        self.tutor = tutor
        self.topic = topic

    def tutor_as_dict(self):
        return {
            "id": self.tutor.id,
            "period_id": self.tutor.period_id,
            "name": self.tutor.name,
            "last_name": self.tutor.last_name,
            "email": self.tutor.email,
        }

    def topic_as_dict(self):
        return {
            "id": self.topic.id,
            "name": self.topic.name,
            "category": self.topic.category,
        }
