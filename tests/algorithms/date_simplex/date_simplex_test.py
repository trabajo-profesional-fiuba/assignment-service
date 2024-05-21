from src.algorithms.date_evaluators_lp import DateEvaluatorsLPSolver
from src.algorithms.date_tutors_lp import DateTutorsLPSolver
import time

from src.model.group.simplex_group import SimplexGroup
from src.model.tutor.simplex_tutor import SimplexTutor
from src.model.utils.evaluator import Evaluator
from tests.algorithms.date_simplex.helper import TestSimplexHelper


class TestDatesSimplex:
    helper = TestSimplexHelper()

    # ------------ Performance and Scalability Tests ------------
    def test_four_groups_and_evaluators(self):
        """Testing if the algorithm is overhead with four groups, four dates and four evaluators."""
        num_groups = 4
        num_evaluators = 4
        num_tutors = 4
        num_dates = 4

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors)
        result = solver.solve()

        solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
        result_evaluators = solver_evaluators.solve()
        end_time = time.time()

        assert len(result) > 0
        assert len(result_evaluators) > 0

        print(
            "4 groups, 4 evaluators, 2 tutors, 4 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_four_evaluators(self):
        """Testing if the algorithm is overhead with ten groups, five dates and five evaluators."""
        num_groups = 10
        num_evaluators = 5
        num_tutors = 5
        num_dates = 5

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors)
        result = solver.solve()

        solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
        result_evaluators = solver_evaluators.solve()
        end_time = time.time()

        assert len(result) > 0
        assert len(result_evaluators) > 0

        print(
            "10 groups, 5 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_one_evaluators(self):
        """Testing if the algorithm is overhead with ten groups, five dates and 1 evaluator."""
        num_groups = 10
        num_evaluators = 1
        num_tutors = 5
        num_dates = 5

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors)
        result = solver.solve()

        solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
        result_evaluators = solver_evaluators.solve()
        end_time = time.time()

        assert len(result) > 0
        assert len(result_evaluators) > 0

        print(
            "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_fifty_groups_and_four_evaluators(self):
        """Testing if the algorithm is overhead with fifty groups, ten dates and four evaluators."""
        num_groups = 50
        num_evaluators = 4
        num_tutors = 6
        num_dates = 10

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors)
        result = solver.solve()

        solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
        result_evaluators = solver_evaluators.solve()
        end_time = time.time()

        assert len(result) > 0
        assert len(result_evaluators) > 0
        print(
            "50 groups, 4 evaluators, 6 tutors, 10 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    # ------------ Logical Tests ------------
    def test_group_evaluator_assignment_maximization(self):
        possible_dates = ["date1", "date2", "date3", "date4", "date5"]
        groups = [
            SimplexGroup(
                group_id="g1", available_dates=["date1", "date2"], tutor_id="t1"
            ),
            SimplexGroup(
                group_id="g2", available_dates=["date2", "date3"], tutor_id="t2"
            ),
            SimplexGroup(
                group_id="g3", available_dates=["date3", "date4"], tutor_id="t3"
            ),
            SimplexGroup(
                group_id="g4", available_dates=["date4", "date5"], tutor_id="t1"
            ),
            SimplexGroup(
                group_id="g5", available_dates=["date1", "date5"], tutor_id="t2"
            ),
        ]
        tutors = [
            SimplexTutor(id="t1", available_dates=["date1", "date4", "date5"]),
            SimplexTutor(id="t2", available_dates=["date2", "date3", "date5"]),
            SimplexTutor(id="t3", available_dates=["date3", "date4"]),
        ]
        evaluators = [
            Evaluator(id="e1", available_dates=["date1", "date2"]),
            Evaluator(id="e2", available_dates=["date2", "date3"]),
            Evaluator(id="e3", available_dates=["date3", "date4"]),
            Evaluator(id="e4", available_dates=["date4", "date5"]),
        ]

        solver = DateTutorsLPSolver(possible_dates, groups, tutors)
        result = solver.solve()

        solver_evaluators = DateEvaluatorsLPSolver(possible_dates, result, evaluators)
        result_evaluators = solver_evaluators.solve()

        # Comprueba que todos los grupos tienen evaluadores asignados
        group_assignments = {group.id: 0 for group in groups}
        for var in result_evaluators:
            group_assignments[var[0]] += 1

        for group_id in group_assignments:
            assert 1 <= group_assignments[group_id] <= 4

        # Comprueba que la cantidad máxima de grupos evaluados por día no se exceda
        evaluator_date_count = {}
        for var in result_evaluators:
            evaluator_date_count[(var[2], var[1])] = (
                evaluator_date_count.get((var[2], var[1]), 0) + 1
            )

        for key in evaluator_date_count:
            assert evaluator_date_count[key] <= 5
