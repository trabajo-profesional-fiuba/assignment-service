from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.utils.evaluator import Evaluator


class AssignmentResult:

    def __init__(
        self,
        id: int,
        groups: list[Group],
        tutors: list[Tutor],
        evaluators: list[Evaluator] = None,
    ) -> None:
        self._id: id
        self._groups: groups
        self._tutors: tutors
        self._evaluators: evaluators
