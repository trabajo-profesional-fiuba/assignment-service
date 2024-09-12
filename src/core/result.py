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

    def __init__(self, id, tutor_email, topic) -> None:
        self.id = id
        self.tutor_email = tutor_email
        self.topic = topic
