from solver import Solver


class GroupTutorSolver(Solver):

    def __init__(self, groups, tutors, formatter, topics, available_dates):
        super().__init__(groups, tutors, formatter)
        self._topics = available_dates
