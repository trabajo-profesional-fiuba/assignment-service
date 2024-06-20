from src.assignments.date.delivery_solver import DeliverySolver
from src.assignments.date.lp.delivery_tutors_lp_solver import DeliveryTutorsLPSolver
from src.assignments.date.lp.delivery_evaluators_lp_solver import DateEvaluatorsLPSolver
from src.io.output.result_context import ResultContext


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

        result_context = ResultContext(
            type="linear",
            result=result_evaluators,
            groups=self._groups,
            evaluators=self._evaluators,
        )
        assignment_result = self._formatter.format_result(result_context)

        return assignment_result
