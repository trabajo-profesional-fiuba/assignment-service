from src.algorithms.solver import Solver


class DeliverySolver(Solver):

    def __init__(self, groups, tutors, formatter, avaliable_dates):
        super().__init__(groups, tutors, formatter)
        self._avaliable_dates = avaliable_dates
