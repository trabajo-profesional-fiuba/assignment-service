from src.algorithms.delivery_evaluators_lp_solver import DateEvaluatorsLPSolver
from src.algorithms.delivery_lp_solver import DeliveryLPSolver
from src.algorithms.delivery_tutors_lp_solver import DeliveryTutorsLPSolver
import time

from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.final_state_tutor import FinalStateTutor
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
        days_per_week = ["lunes", "martes", "miercoles", "jueves", "viernes"]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        start_time = time.time()
        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)
        
        solver = DeliveryLPSolver(groups, tutors, None, dates, evaluators)
        result = solver.solve()
        # solver = DeliveryTutorsLPSolver(dates, groups, tutors, num_weeks)
        # result = solver.solve()

        # solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
        # result_evaluators = solver_evaluators.solve()
        end_time = time.time()

        assert len(result) > 0

        print(
            "4 groups, 4 evaluators, 2 tutors, 4 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    # def test_ten_groups_and_four_evaluators(self):
    #     """Testing if the algorithm is overhead with ten groups, five dates and five evaluators."""
    #     num_groups = 10
    #     num_evaluators = 5
    #     num_tutors = 5

    #     num_weeks = 7  
    #     days_per_week = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    #     hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    #     start_time = time.time()
    #     dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
    #     groups = self.helper.create_groups(num_groups, dates)
    #     tutors = self.helper.create_tutors(num_tutors, dates)
    #     evaluators = self.helper.create_evaluators(num_evaluators, dates)
    #     solver = DeliveryTutorsLPSolver(dates, groups, tutors, num_weeks)
    #     result = solver.solve()

    #     solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
    #     result_evaluators = solver_evaluators.solve()
    #     end_time = time.time()

    #     assert len(result) > 0
    #     assert len(result_evaluators) > 0

    #     print(
    #         "10 groups, 5 evaluators, 5 tutors, 5 dates - Execution time:",
    #         end_time - start_time,
    #         "seconds",
    #     )

    # def test_ten_groups_and_one_evaluators(self):
    #     """Testing if the algorithm is overhead with ten groups, five dates and 1 evaluator."""
    #     num_groups = 10
    #     num_evaluators = 1
    #     num_tutors = 5

    #     num_weeks = 7  
    #     days_per_week = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    #     hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    #     start_time = time.time()
    #     dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
    #     groups = self.helper.create_groups(num_groups, dates)
    #     tutors = self.helper.create_tutors(num_tutors, dates)
    #     evaluators = self.helper.create_evaluators(num_evaluators, dates)
    #     solver = DeliveryTutorsLPSolver(dates, groups, tutors, num_weeks)
    #     result = solver.solve()

    #     solver_evaluators = DateEvaluatorsLPSolver(dates, result, evaluators)
    #     result_evaluators = solver_evaluators.solve()
    #     end_time = time.time()

    #     assert len(result) > 0
    #     assert len(result_evaluators) > 0

    #     print(
    #         "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
    #         end_time - start_time,
    #         "seconds",
    #     )

    # def test_fifty_groups_and_four_evaluators(self):
    #     """Testing if the algorithm is overhead with fifty groups, ten dates and four evaluators."""
    #     num_groups = 50
    #     num_evaluators = 4
    #     num_tutors = 6

    #     num_weeks = 7  
    #     days_per_week = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    #     hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

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
    # def test_group_evaluator_assignment_maximization(self):
    #     possible_dates = [DateDto( 1,"lunes", 1), DateDto( 1, "lunes",2), DateDto( 1,"lunes", 3), DateDto( 1,"lunes", 4), DateDto( 1, "lunes",5), DateDto( 1, "lunes",6), DateDto( 1,"lunes", 7), DateDto( 1, "lunes",8),
    #                       DateDto( 1, "lunes",9), DateDto( 1, "lunes",10), DateDto( 1,"lunes", 11),
    #                       DateDto( 2, "martes",1), DateDto( 2, "martes",2), DateDto(2,"martes",  3), DateDto(2,"martes",  4), DateDto(2,"martes",  5), DateDto(2,"martes",  6), DateDto(2,"martes",  7),
    #                       DateDto( 2,"martes", 8), DateDto( 2,"martes", 9), DateDto( 2,"martes", 10), DateDto( 2,"martes", 11),
    #                       DateDto( 3,"miercoles", 1), DateDto( 3,"miercoles", 2), DateDto( 3,"miercoles", 3), DateDto( 3,"miercoles", 4), DateDto( 3,"miercoles", 5), DateDto( 3,"miercoles", 6), DateDto( 3,"miercoles", 7),
    #                       DateDto( 3,"miercoles", 8), DateDto( 3,"miercoles", 9), DateDto( 3,"miercoles", 10), DateDto( 3,"miercoles", 11),
    #                       DateDto( 4,"miercoles", 1), DateDto( 4,"miercoles", 2), DateDto( 4,"miercoles", 3), DateDto( 4,"miercoles", 4), DateDto("miercoles", 4, 5), DateDto("miercoles", 4, 6), DateDto("miercoles", 4, 7),
    #                       DateDto( 4,"miercoles", 8), DateDto( 4,"miercoles", 9), DateDto( 4,"miercoles", 10), DateDto( 4,"miercoles", 11),
    #                       DateDto(5,"friday", 1), DateDto(5,"friday", 2), DateDto(5,"friday", 3), DateDto(5,"friday", 4), DateDto(5,"friday", 5), DateDto(5,"friday", 6), DateDto(5,"friday", 7), DateDto(5,"friday", 8),
    #                       DateDto(5,"friday", 9), DateDto(5,"friday", 10), DateDto(5,"friday", 11)]
        
    #     groups = [
    #         FinalStateGroup(
    #             group_id="g1", available_dates=possible_dates[0:22], tutor_id="t1"
    #         ),
    #         FinalStateGroup(
    #             group_id="g2", available_dates=possible_dates[11:33], tutor_id="t2"
    #         ),
    #         FinalStateGroup(
    #             group_id="g3", available_dates=possible_dates[22:44], tutor_id="t3"
    #         ),
    #         FinalStateGroup(
    #             group_id="g4", available_dates=possible_dates[33:55], tutor_id="t1"
    #         ),
    #         FinalStateGroup(
    #             group_id="g5", available_dates=possible_dates[0:11]+possible_dates[44:55], tutor_id="t2"
    #         ),
    #     ]
    #     tutors = [
    #         FinalStateTutor(id="t1", available_dates=possible_dates[0:11]+possible_dates[33:44]+ possible_dates[44:55]) ,
    #         FinalStateTutor(id="t2", available_dates=possible_dates[11:22]+possible_dates[22:33]+possible_dates[44:55]),
    #         FinalStateTutor(id="t3", available_dates=possible_dates[22:33]+possible_dates[33:44]),
    #     ]
    #     evaluators = [
    #         Evaluator(id="e1", available_dates=possible_dates[0:22]),
    #         Evaluator(id="e2", available_dates=possible_dates[11:33]),
    #         Evaluator(id="e3", available_dates=possible_dates[22:44]),
    #         Evaluator(id="e4", available_dates=possible_dates[33:55]),
    #     ]

    #     solver = DeliveryTutorsLPSolver(possible_dates, groups, tutors, 5)
    #     result = solver.solve()

    #     solver_evaluators = DateEvaluatorsLPSolver(possible_dates, result, evaluators)
    #     result_evaluators = solver_evaluators.solve()

    #     # Comprueba que todos los grupos tienen evaluadores asignados
    #     group_assignments = {group.id: 0 for group in groups}
    #     for var in result_evaluators:
    #         group_assignments[var[0]] += 1

    #     for group_id in group_assignments:
    #         assert 1 <= group_assignments[group_id] <= 4

    #     # Comprueba que la cantidad máxima de grupos evaluados por día no se exceda
    #     evaluator_date_count = {}
    #     for var in result_evaluators:
    #         evaluator_date_count[(var[2], var[1])] = (
    #             evaluator_date_count.get((var[2], var[1]), 0) + 1
    #         )

    #     for key in evaluator_date_count:
    #         assert evaluator_date_count[key] <= 5
