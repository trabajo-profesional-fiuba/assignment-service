import time
import pytest

from src.algorithms.delivery_lp_solver import DeliveryLPSolver
from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator
from tests.algorithms.date_simplex.helper import TestLPHelper
from src.model.formatter.output.output_formatter import OutputFormatter


class TestDatesSimplex:
    helper = TestLPHelper()
    formatter = OutputFormatter()

    # ------------ Performance and Scalability Tests ------------
    @pytest.mark.performance
    def test_four_groups_and_evaluators(self):
        """Testing if the algorithm is overhead with four groups,
        four dates and four evaluators."""
        num_groups = 4
        num_evaluators = 4
        num_tutors = 4
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, self.formatter, dates, evaluators)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.groups) > 0

        print(
            "4 groups, 4 evaluators, 2 tutors, 4 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    @pytest.mark.performance
    def test_ten_groups_and_four_evaluators(self):
        """Testing if the algorithm is overhead with ten groups,
        five dates and five evaluators."""
        num_groups = 10
        num_evaluators = 5
        num_tutors = 5

        num_weeks = 7
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, self.formatter, dates, evaluators)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.groups) > 0

        print(
            "10 groups, 5 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    @pytest.mark.performance
    def test_ten_groups_and_one_evaluator(self):
        """Testing if the algorithm is overhead with ten groups,
        five dates and 1 evaluator."""
        num_groups = 10
        num_evaluators = 1
        num_tutors = 5

        num_weeks = 7
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        solver = DeliveryLPSolver(groups, tutors, self.formatter, dates, evaluators)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.groups) > 0

        print(
            "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    # @pytest.mark.performance
    # def test_fifty_groups_and_four_evaluators(self):
    #     """Testing if the algorithm is overhead with fifty groups,
    #     ten dates and four evaluators."""
    #     num_groups = 50
    #     num_evaluators = 4
    #     num_tutors = 6

    #     num_weeks = 7
    #     days_per_week = [1, 2, 3, 4, 5]
    #     hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    #     dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
    #     groups = self.helper.create_groups(num_groups, dates)
    #     tutors = self.helper.create_tutors(num_tutors, dates)

    #     evaluators = self.helper.create_evaluators(num_evaluators, dates)
    #     solver = DeliveryLPSolver(groups, tutors, self.formatter, dates, evaluators)
    #     start_time = time.time()
    #     result = solver.solve()
    #     end_time = time.time()

    #     assert len(result.groups) > 0
    #     print(
    #         "50 groups, 4 evaluators, 6 tutors, 10 dates - Execution time:",
    #         end_time - start_time,
    #         "seconds",
    #     )

    # ------------ Logical Tests ------------
    @pytest.mark.unit
    def test_all_groups_are_assigned_evaluators(self):
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

        tutor1 = Tutor(1, "Tutor 1", "email@tutor1.com")
        tutor1.add_available_dates(
            possible_dates[0:11] + possible_dates[33:44] + possible_dates[44:55]
        )
        tutor2 = Tutor(2, "Tutor 2", "email@tutor2.com")
        tutor2.add_available_dates(
            possible_dates[11:22] + possible_dates[22:33] + possible_dates[44:55]
        )
        tutor3 = Tutor(3, "Tutor 3", "email@tutor3.com")
        tutor3.add_available_dates(possible_dates[22:33] + possible_dates[33:44])
        group1 = Group(1, tutor1)
        group1.add_available_dates(possible_dates[0:22])
        group2 = Group(2, tutor2)
        group2.add_available_dates(possible_dates[11:33])
        group3 = Group(3, tutor3)
        group3.add_available_dates(possible_dates[22:44])
        group4 = Group(4, tutor1)
        group4.add_available_dates(possible_dates[33:55])
        group5 = Group(5, tutor3)
        group5.add_available_dates(possible_dates[0:11] + possible_dates[33:44])
        groups = [group1, group2, group3, group4, group5]
        tutors = [tutor1, tutor2, tutor3]
        evaluators = [
            Evaluator(id=11, available_dates=possible_dates[0:22]),
            Evaluator(id=12, available_dates=possible_dates[11:33]),
            Evaluator(id=13, available_dates=possible_dates[22:44]),
            Evaluator(id=14, available_dates=possible_dates[33:55]),
        ]

        solver = DeliveryLPSolver(
            groups, tutors, self.formatter, possible_dates, evaluators
        )
        result = solver.solve()

        # Check that all groups have assigned evaluators
        group_assignments = {group.id: 0 for group in result.groups}
        for group in result.groups:
            for evaluator in result.evaluators:
                for assigned_date in result.delivery_date_evaluator(evaluator):
                    if (
                        assigned_date.label()
                        == result.delivery_date_group(group).label()
                    ):
                        group_assignments[group.id] += 1

        for group_id, evaluators_assigned in group_assignments.items():
            assert 1 <= evaluators_assigned <= 4

        # # Check that the max number of groups per day is not exceeded
        # evaluator_date_count = {}
        # for var in result.groups:
        #     evaluator_date_count[(var[2], var[1])] = (
        #         evaluator_date_count.get((var[2], var[1]), 0) + 1
        #     )

        # for key in evaluator_date_count:
        #     assert evaluator_date_count[key] <= 5
