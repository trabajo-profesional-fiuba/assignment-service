from src.algorithms.solver import Solver


class DeliverySolver(Solver):

    def __init__(self, groups, tutors, formatter, available_dates):
        super().__init__(groups, tutors, formatter)
        self._available_dates = available_dates
