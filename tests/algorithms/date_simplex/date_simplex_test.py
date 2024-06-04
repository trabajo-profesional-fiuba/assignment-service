from src.algorithms.delivery_lp_solver import DeliveryLPSolver
import time

from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evalutor import Evaluator
from tests.algorithms.date_simplex.helper import TestSimplexHelper


class TestDatesSimplex:
    helper = TestSimplexHelper()

    # ------------ Performance and Scalability Tests ------------
    def test_four_groups_and_evaluators(self):
        """Testing if the algorithm is overhead with four groups,
        four dates and four evaluators."""
        num_groups = 4
        num_evaluators = 4
        num_tutors = 4
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, None, dates, evaluators)
        result = solver.solve()

        end_time = time.time()

        assert len(result) > 0

        print(
            "4 groups, 4 evaluators, 2 tutors, 4 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_four_evaluators(self):
        """Testing if the algorithm is overhead with ten groups,
        five dates and five evaluators."""
        num_groups = 10
        num_evaluators = 5
        num_tutors = 5

        num_weeks = 7
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, None, dates, evaluators)
        result = solver.solve()

        end_time = time.time()

        assert len(result) > 0

        print(
            "10 groups, 5 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    def test_ten_groups_and_one_evaluators(self):
        """Testing if the algorithm is overhead with ten groups,
        five dates and 1 evaluator."""
        num_groups = 10
        num_evaluators = 1
        num_tutors = 5

        num_weeks = 7
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, None, dates, evaluators)
        result = solver.solve()

        end_time = time.time()

        assert len(result) > 0

        print(
            "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    # def test_fifty_groups_and_four_evaluators(self):
    #     """Testing if the algorithm is overhead with fifty groups,
    #     ten dates and four evaluators."""
    #     num_groups = 50
    #     num_evaluators = 4
    #     num_tutors = 6

    #     num_weeks = 7
    #     days_per_week = [1, 2, 3, 4, 5]
    #     hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    #     start_time = time.time()
    #     dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
    #     groups = self.helper.create_groups(num_groups, dates)
    #     tutors = self.helper.create_tutors(num_tutors, dates)

    #     evaluators = self.helper.create_evaluators(num_evaluators, dates)
    #     solver = DeliveryLPSolver(groups, tutors, None, dates, evaluators)
    #     result = solver.solve()

    #     end_time = time.time()

    #     assert len(result) > 0
    #     print(
    #         "50 groups, 4 evaluators, 6 tutors, 10 dates - Execution time:",
    #         end_time - start_time,
    #         "seconds",
    #     )

    # ------------ Logical Tests ------------
    def test_group_evaluator_assignment_maximization(self):
        possible_dates = [
            DeliveryDate(1, 1, 1),
            DeliveryDate(1, 1, 2),
            DeliveryDate(1, 1, 3),
            DeliveryDate(1, 1, 4),
            DeliveryDate(1, 1, 5),
            DeliveryDate(1, 1, 6),
            DeliveryDate(1, 1, 7),
            DeliveryDate(1, 1, 8),
            DeliveryDate(1, 1, 9),
            DeliveryDate(1, 1, 10),
            DeliveryDate(1, 1, 11),
            DeliveryDate(2, 2, 1),
            DeliveryDate(2, 2, 2),
            DeliveryDate(2, 2, 3),
            DeliveryDate(2, 2, 4),
            DeliveryDate(2, 2, 5),
            DeliveryDate(2, 2, 6),
            DeliveryDate(2, 2, 7),
            DeliveryDate(2, 2, 8),
            DeliveryDate(2, 2, 9),
            DeliveryDate(2, 2, 10),
            DeliveryDate(2, 2, 11),
            DeliveryDate(3, 3, 1),
            DeliveryDate(3, 3, 2),
            DeliveryDate(3, 3, 3),
            DeliveryDate(3, 3, 4),
            DeliveryDate(3, 3, 5),
            DeliveryDate(3, 3, 6),
            DeliveryDate(3, 3, 7),
            DeliveryDate(3, 3, 8),
            DeliveryDate(3, 3, 9),
            DeliveryDate(3, 3, 10),
            DeliveryDate(3, 3, 11),
            DeliveryDate(4, 3, 1),
            DeliveryDate(4, 3, 2),
            DeliveryDate(4, 3, 3),
            DeliveryDate(4, 3, 4),
            DeliveryDate(3, 4, 5),
            DeliveryDate(3, 4, 6),
            DeliveryDate(3, 4, 7),
            DeliveryDate(4, 3, 8),
            DeliveryDate(4, 3, 9),
            DeliveryDate(4, 3, 10),
            DeliveryDate(4, 3, 11),
            DeliveryDate(5, 5, 1),
            DeliveryDate(5, 5, 2),
            DeliveryDate(5, 5, 3),
            DeliveryDate(5, 5, 4),
            DeliveryDate(5, 5, 5),
            DeliveryDate(5, 5, 6),
            DeliveryDate(5, 5, 7),
            DeliveryDate(5, 5, 8),
            DeliveryDate(5, 5, 9),
            DeliveryDate(5, 5, 10),
            DeliveryDate(5, 5, 11),
        ]

        tutor1 = Tutor(1, "Nombre Tutor 1", "email@tutor1.com")
        tutor1.add_available_dates(
            possible_dates[0:11] + possible_dates[33:44] + possible_dates[44:55]
        )
        tutor2 = Tutor(2, "Nombre Tutor 2", "email@tutor2.com")
        tutor2.add_available_dates(
            possible_dates[11:22] + possible_dates[22:33] + possible_dates[44:55]
        )
        tutor3 = Tutor(3, "Nombre Tutor 3", "email@tutor3.com")
        tutor3.add_available_dates(possible_dates[22:33] + possible_dates[33:44])
        group1 = Group("g1", tutor1)
        group1.add_available_dates(possible_dates[0:22])
        group2 = Group("g2", tutor2)
        group2.add_available_dates(possible_dates[11:33])
        group3 = Group("g3", tutor3)
        group3.add_available_dates(possible_dates[22:44])
        group4 = Group("g4", tutor1)
        group4.add_available_dates(possible_dates[33:55])
        group5 = Group("g5", tutor3)
        group5.add_available_dates(possible_dates[0:11] + possible_dates[33:44])
        groups = [group1, group2, group3, group4, group5]
        tutors = [tutor1, tutor2, tutor3]
        evaluators = [
            Evaluator(id=11, available_dates=possible_dates[0:22]),
            Evaluator(id=12, available_dates=possible_dates[11:33]),
            Evaluator(id=13, available_dates=possible_dates[22:44]),
            Evaluator(id=14, available_dates=possible_dates[33:55]),
        ]

        solver = DeliveryLPSolver(groups, tutors, None, possible_dates, evaluators)
        result = solver.solve()

        # Comprueba que todos los grupos tienen evaluadores asignados
        group_assignments = {group.id: 0 for group in groups}
        for var in result:
            group_assignments[var[0]] += 1
        print(result)
        print(group_assignments)
        for group_id in group_assignments:
            assert 1 <= group_assignments[group_id] <= 4

        # Comprueba que la cantidad máxima de grupos evaluados por día no se exceda
        evaluator_date_count = {}
        for var in result:
            evaluator_date_count[(var[2], var[1])] = (
                evaluator_date_count.get((var[2], var[1]), 0) + 1
            )

        for key in evaluator_date_count:
            assert evaluator_date_count[key] <= 5
