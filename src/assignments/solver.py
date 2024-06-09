from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.io.output.output_formatter import OutputFormatter


class Solver:
    def __init__(
        self, groups: list[Group], tutors: list[Tutor], formatter: OutputFormatter
    ):
        self._groups = groups
        self._tutors = tutors
        self._formatter = formatter

    def solve():
        # this should be an exception then
        pass
