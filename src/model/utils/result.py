class AssignmentResult:

    def __init__(self, results, substitutes: None) -> None:
        self._results = results
        self._substitutes = substitutes

    def get_result(self):
        return self._results

    def get_substitutes(self):
        return self._substitutes
