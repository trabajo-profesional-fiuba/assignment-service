from src.model.group.group import Group
from src.model.utils.evaluator import Evaluator


class AssignmentResult:

    def __init__(self, groups: list[Group], evaluators: list[Evaluator]) -> None:
        self._groups = groups
        self._evaluators = evaluators

    @property
    def groups(self):
        return self._groups

    @property
    def evaluators(self):
        return self._evaluators

    def delivery_date_group(self, group):
        return group.assigned_date()

    def delivery_date_evaluator(self, evaluator):
        return evaluator.assigned_dates
