from src.algorithms.date_simplex import DateSimplexSolver
import time

from tests.algorithms.date_simplex.helper import TestSimplexHelper


class TestDatesSimplex:
    helper = TestSimplexHelper()

    # ------------ Performance and Scalability Tests ------------
    def test_four_groups_and_evaluators(self):
        """Testing if the algorithm is overhead with four groups and topics."""
        num_groups = 4
        num_evaluators = 4
        num_tutors = 4
        num_dates = 4

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateSimplexSolver(dates, groups, tutors, evaluators)
        result = solver.solve()
        end_time = time.time()

        assert len(result) > 0
        print(
            "4 groups, 4 evaluators, 2 tutors, 4 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_four_evaluators(self):
        """Testing if the algorithm is overhead with four groups and topics."""
        num_groups = 10
        num_evaluators = 5
        num_tutors = 5
        num_dates = 5

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateSimplexSolver(dates, groups, tutors, evaluators)
        result = solver.solve()
        end_time = time.time()

        assert len(result) > 0
        print(
            "10 groups, 5 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_one_evaluators(self):
        """Testing if the algorithm is overhead with four groups and topics."""
        num_groups = 10
        num_evaluators = 1
        num_tutors = 5
        num_dates = 5

        start_time = time.time()
        dates = self.helper.create_dates(num_dates)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateSimplexSolver(dates, groups, tutors, evaluators)
        result = solver.solve()
        end_time = time.time()

        assert len(result) > 0
        print(
            "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )
