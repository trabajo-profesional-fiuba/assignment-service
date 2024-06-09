from solver import Solver
from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.topic import Topic
from src.model.formatter.output.output_formatter import OutputFormatter


class GroupTutorSolver(Solver):

    def __init__(
        self,
        groups: list[Group],
        tutors: list[Tutor],
        formatter: OutputFormatter,
        topics: list[Topic],
    ):
        super().__init__(groups, tutors, formatter)
        self._topics = topics
