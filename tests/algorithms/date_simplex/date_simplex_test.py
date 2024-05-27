from src.algorithms.date_evaluators_lp import DateEvaluatorsLPSolver
from src.algorithms.date_tutors_lp import DateTutorsLPSolver
import time

from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.model.utils.date import Date
from src.model.utils.day import Day
from src.model.utils.evaluator import Evaluator
from src.model.utils.hour import Hour
from tests.algorithms.date_simplex.helper import TestSimplexHelper


class TestDatesSimplex:
    helper = TestSimplexHelper()

    # ------------ Performance and Scalability Tests ------------
    def test_four_groups_and_evaluators(self):
        """Testing if the algorithm is overhead with four groups, four dates and four evaluators."""
        num_groups = 4
        num_evaluators = 4
        num_tutors = 4
        num_weeks = 4 
        days_per_week = [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]
        hours_per_day = [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors, num_weeks)
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

        num_weeks = 7  
        days_per_week = [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]
        hours_per_day = [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors, num_weeks)
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

        num_weeks = 7  
        days_per_week = [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]
        hours_per_day = [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        solver = DateTutorsLPSolver(dates, groups, tutors, num_weeks)
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

    # def test_fifty_groups_and_four_evaluators(self):
    #     """Testing if the algorithm is overhead with fifty groups, ten dates and four evaluators."""
    #     num_groups = 50
    #     num_evaluators = 4
    #     num_tutors = 6

    #     num_weeks = 7  
    #     days_per_week = [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]
    #     hours_per_day = [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]

    #     start_time = time.time()
    #     dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
    #     groups = self.helper.create_groups(num_groups, dates)
    #     tutors = self.helper.create_tutors(num_tutors, dates)
    #     evaluators = self.helper.create_evaluators(num_evaluators, dates)
    #     solver = DateTutorsLPSolver(dates, groups, tutors, num_weeks)
    #     result = solver.solve()

    #     solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
    #     result_evaluators = solver_evaluators.solve()
    #     end_time = time.time()

    #     assert len(result) > 0
    #     assert len(result_evaluators) > 0
    #     print(
    #         "50 groups, 4 evaluators, 6 tutors, 10 dates - Execution time:",
    #         end_time - start_time,
    #         "seconds",
    #     )

    # ------------ Logical Tests ------------
    def test_group_evaluator_assignment_maximization(self):
        possible_dates = [Date(Day.MONDAY, 1, [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]),
                          Date(Day.TUESDAY, 2, [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]),
                          Date(Day.WEDNESDAY, 3, [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]),
                          Date(Day.WEDNESDAY, 4, [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21]),
                          Date(Day.FRIDAY, 5, [Hour.H_9_10, Hour.H_10_11, Hour.H_11_12, Hour.H_12_13, Hour.H_14_15, Hour.H_15_16, Hour.H_16_17, Hour.H_17_18, Hour.H_18_19, Hour.H_19_20, Hour.H_20_21])]
        groups = [
            FinalStateGroup(
                group_id="g1", available_dates=[possible_dates[0], possible_dates[1]], tutor_id="t1"
            ),
            FinalStateGroup(
                group_id="g2", available_dates=[possible_dates[1], possible_dates[2]], tutor_id="t2"
            ),
            FinalStateGroup(
                group_id="g3", available_dates=[possible_dates[2], possible_dates[3]], tutor_id="t3"
            ),
            FinalStateGroup(
                group_id="g4", available_dates=[possible_dates[3], possible_dates[4]], tutor_id="t1"
            ),
            FinalStateGroup(
                group_id="g5", available_dates=[possible_dates[0], possible_dates[4]], tutor_id="t2"
            ),
        ]
        tutors = [
            FinalStateTutor(id="t1", available_dates=[possible_dates[0], possible_dates[3], possible_dates[4]]),
            FinalStateTutor(id="t2", available_dates=[possible_dates[1], possible_dates[2], possible_dates[4]]),
            FinalStateTutor(id="t3", available_dates=[possible_dates[2], possible_dates[3]]),
        ]
        evaluators = [
            Evaluator(id="e1", available_dates=[possible_dates[0], possible_dates[1]]),
            Evaluator(id="e2", available_dates=[possible_dates[1], possible_dates[2]]),
            Evaluator(id="e3", available_dates=[possible_dates[2], possible_dates[3]]),
            Evaluator(id="e4", available_dates=[possible_dates[3], possible_dates[4]]),
        ]

        solver = DateTutorsLPSolver(possible_dates, groups, tutors, 5)
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
