from src.model.group import Group
from src.model.tutor import Tutor
from src.assignments.adapters.result_adapter import ResultAdapter


class Solver:
    def __init__(
        self, groups: list[Group], tutors: list[Tutor], formatter: ResultAdapter
    ):
        self._groups = groups
        self._tutors = tutors
        self._formatter = formatter

    def solve():
        # this should be an exception then
        pass
