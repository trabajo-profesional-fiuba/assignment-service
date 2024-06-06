from src.algorithms.delivery_evaluators_lp_solver import DateEvaluatorsLPSolver
from src.algorithms.delivery_solver import DeliverySolver
from src.algorithms.delivery_tutors_lp_solver import DeliveryTutorsLPSolver


class DeliveryLPSolver(DeliverySolver):
    def __init__(self, groups, tutors, formatter, available_dates, evaluators):
        super().__init__(groups, tutors, formatter, available_dates)
        self._evaluators = evaluators

    def solve(self):
        solver_tutors = DeliveryTutorsLPSolver(
            self._available_dates, self._groups, self._tutors
        )
        result_tutors = solver_tutors.solve()

        solver_evaluators = DateEvaluatorsLPSolver(
            self._available_dates, result_tutors, self._groups, self._evaluators
        )
        result_evaluators = solver_evaluators.solve()

        assignment_result = self._formatter.format_result(
            result_evaluators, self._groups, self._evaluators
        )

        return assignment_result
