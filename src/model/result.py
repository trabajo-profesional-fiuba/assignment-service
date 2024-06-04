from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.utils.evaluator import Evaluator


class AssignmentResult:

    def __init__(
        self,
        groups: list[Group],
    ) -> None:
        self._groups: groups
