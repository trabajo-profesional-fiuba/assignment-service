from solver import Solver
from src.model.group import Group
from src.model.tutor import Tutor
from src.model.utils.topic import Topic
from src.algorithms.adapters.result_adapter import ResultAdapter


class GroupTutorSolver(Solver):

    def __init__(
        self,
        groups: list[Group],
        tutors: list[Tutor],
        formatter: ResultAdapter,
        topics: list[Topic],
    ):
        super().__init__(groups, tutors, formatter)
        self._topics = topics