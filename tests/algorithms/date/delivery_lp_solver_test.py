import time
import pytest

from src.algorithms.adapters.result_adapter import ResultAdapter

from src.algorithms.date.delivery_lp_solver import DeliveryLPSolver
from src.model.group import Group
from src.model.period import TutorPeriod
from src.model.tutor import Tutor
from src.model.utils.delivery_date import DeliveryDate
from tests.algorithms.date.helper import TestLPHelper


class TestDeliveryLPSolver:
    helper = TestLPHelper()
    adapter = ResultAdapter()

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

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.get_results()) == 4

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

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.get_results()) == num_groups

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

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        start_time = time.time()
        result = solver.solve()
        end_time = time.time()

        assert len(result.get_results()) == num_groups

        print(
            "10 groups, 1 evaluators, 5 tutors, 5 dates - Execution time:",
            end_time - start_time,
            "seconds",
        )

    # @pytest.mark.skip
    # def test_fifty_groups_and_four_evaluators(self):
    #     Testing if the algorithm is overhead with fifty groups,
    #     ten dates and four evaluators.
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

        tutor_period1 = TutorPeriod("1C2024")
        tutor1 = Tutor(1, "Tutor 1", "email@tutor1.com")
        tutor_period1.add_parent(tutor1)
        tutor_period1.add_available_dates(
            possible_dates[0:11] + possible_dates[33:44] + possible_dates[44:55]
        )

        tutor_period2 = TutorPeriod("1C2024")
        tutor2 = Tutor(2, "Tutor 2", "email@tutor2.com")
        tutor_period2.add_parent(tutor2)
        tutor_period2.add_available_dates(
            possible_dates[11:22] + possible_dates[22:33] + possible_dates[44:55]
        )

        tutor_period3 = TutorPeriod("1C2024")
        tutor3 = Tutor(3, "Tutor 3", "email@tutor3.com")
        tutor_period3.add_parent(tutor3)
        tutor_period3.add_available_dates(possible_dates[22:33] + possible_dates[33:44])

        group1 = Group(1)
        group1.add_available_dates(possible_dates[0:22])
        group2 = Group(2)
        group2.add_available_dates(possible_dates[11:33])
        group3 = Group(3)
        group3.add_available_dates(possible_dates[22:44])
        group4 = Group(4)
        group4.add_available_dates(possible_dates[33:55])
        group5 = Group(5)
        group5.add_available_dates(possible_dates[0:11] + possible_dates[33:44])

        tutor_period1.add_groups([group1, group4])
        tutor_period2.add_groups([group2])
        tutor_period3.add_groups([group3, group5])

        tutors = [tutor_period1, tutor_period2, tutor_period3]

        evaluator1 = TutorPeriod("1C2024")
        evaluator1.add_parent(Tutor(11, "email", "name"))
        evaluator1.make_evaluator()
        evaluator1.add_available_dates(possible_dates[0:22])

        evaluator2 = TutorPeriod("1C2024")
        evaluator2.add_parent(Tutor(12, "email", "name"))
        evaluator2.make_evaluator()
        evaluator2.add_available_dates(possible_dates[11:33])

        evaluator3 = TutorPeriod("1C2024")
        evaluator3.add_parent(Tutor(13, "email", "name"))
        evaluator3.make_evaluator()
        evaluator3.add_available_dates(possible_dates[22:44])

        evaluator4 = TutorPeriod("1C2024")
        evaluator4.add_parent(Tutor(14, "email", "name"))
        evaluator4.make_evaluator()
        evaluator4.add_available_dates(possible_dates[33:55])

        evaluators = [evaluator1, evaluator2, evaluator3, evaluator4]

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, possible_dates)
        result = solver.solve()

        group_assignments = {}

        # Inicializar todos los contadores de grupo en 0
        for group, evaluator, date in result.get_results():
            if group not in group_assignments:
                group_assignments[group] = 0

        # Contar las asignaciones para cada grupo
        for group, evaluator, date in result.get_results():
            group_assignments[group] += 1

        # Verificar que cada grupo tenga entre 1 y 4 evaluadores asignados
        for group_id, evaluators_assigned in group_assignments.items():
            assert (
                1 <= evaluators_assigned <= 4
            ), f"Group {group_id} has {evaluators_assigned} evaluators assigned, which\
            is out of allowed range."

        # Inicializar un diccionario para contar asignaciones por evaluador y día
        evaluators_assignment = {
            (evaluator, day_id): 0
            for evaluator in {evaluator for _, evaluator, _ in result.get_results()}
            for day_id in range(1, 6)
        }

        # Contar las asignaciones por evaluador y día
        for group, evaluator, date in result.get_results():
            day_id = int(date.split("-")[2])
            evaluators_assignment[(evaluator, day_id)] += 1

        # Verificar que cada evaluador no tenga más de 5 grupos asignados por día
        for (evaluator_id, day_id), value in evaluators_assignment.items():
            assert (
                value <= 5
            ), f"Evaluator {evaluator_id} has {value} groups assigned on day {day_id},\
                which exceeds the allowed limit."

    @pytest.mark.unit
    def test_no_available_dates(self):
        """Testing if the algorithm can handle no available dates."""
        num_groups = 2
        num_evaluators = 2
        num_tutors = 2
        num_weeks = 0
        days_per_week = []
        hours_per_day = []

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        result = solver.solve()

        assert len(result.get_results()) == 0

    @pytest.mark.unit
    def test_no_evaluators(self):
        """Testing if the algorithm can handle no evaluators."""
        num_groups = 2
        num_evaluators = 0
        num_tutors = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        result = solver.solve()

        assert len(result.get_results()) == 0

    @pytest.mark.unit
    def test_no_groups(self):
        """Testing if the algorithm can handle no groups."""
        num_groups = 0
        num_evaluators = 2
        num_tutors = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        for tutor in tutors:
            groups_aux = []
            for i in range(1, num_groups + 1):
                for group in groups:
                    if ((i % 4) + 1) == tutor.id() and group.id() == i:
                        groups_aux.append(group)
            tutor.add_groups(groups_aux)

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        result = solver.solve()

        assert len(result.get_results()) == 0

    @pytest.mark.unit
    def test_conflicting_dates(self):
        """Testing if the algorithm can handle conflicting dates."""
        num_groups = 2
        num_evaluators = 2
        num_tutors = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, [])
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(num_evaluators, dates)

        # Create conflicting dates
        group1 = groups[0]
        group2 = groups[1]
        group1.add_available_dates([DeliveryDate(1, 1, 1)])
        group2.add_available_dates([DeliveryDate(1, 1, 1)])

        tutors[0].add_groups([group1])
        tutors[1].add_groups([group2])

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        result = solver.solve()

        assert result is None

    @pytest.mark.unit
    def test_evaluator_availability_constraints(self):
        """Testing if the algorithm can handle evaluator availability constraints."""
        num_groups = 2
        num_evaluators = 1
        num_tutors = 2
        num_weeks = 4
        days_per_week = [1, 2, 3, 4, 5]
        hours_per_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        dates = self.helper.create_dates(num_weeks, days_per_week, hours_per_day)
        groups = self.helper.create_groups(num_groups, dates)
        tutors = self.helper.create_tutors(num_tutors, dates)
        evaluators = self.helper.create_evaluators(
            num_evaluators, [DeliveryDate(1, 1, 1), DeliveryDate(1, 2, 2)]
        )

        tutors[0].add_groups([groups[0]])
        tutors[1].add_groups([groups[1]])

        for e in evaluators:
            tutors.append(e)

        solver = DeliveryLPSolver(tutors, self.adapter, dates)
        result = solver.solve()

        group_assignments = {}

        for group, evaluator, date in result.get_results():
            if group not in group_assignments:
                group_assignments[group] = 0

        for group, evaluator, date in result.get_results():
            group_assignments[group] += 1

        for group_id, evaluators_assigned in group_assignments.items():
            assert (
                evaluators_assigned == 1
            ), f"Group {group_id} has {evaluators_assigned} evaluators assigned, which\
                is out of allowed range."

        # Inicializar un diccionario para contar asignaciones por evaluador y día
        evaluators_assignment = {
            (evaluator, day_id): 0
            for evaluator in {evaluator for _, evaluator, _ in result.get_results()}
            for day_id in range(1, 6)
        }

        # Contar las asignaciones por evaluador y día
        for group, evaluator, date in result.get_results():
            day_id = int(date.split("-")[2])
            evaluators_assignment[(evaluator, day_id)] += 1

        # Verificar que cada evaluador no tenga más de 5 grupos asignados por día
        for (evaluator_id, day_id), value in evaluators_assignment.items():
            assert (
                value <= 5
            ), f"Evaluator {evaluator_id} has {value} groups assigned on day {day_id},\
                which exceeds the allowed limit."

        # Verificar que cada grupo tenga una fecha asignada
        assigned_dates = {
            group: date for group, evaluator, date in result.get_results()
        }
        for group in groups:
            assert (
                f"group-{group.id()}" in assigned_dates
            ), f"Group {group.id()} does not have an assigned date."

        # Verificar que las fechas asignadas estén dentro de las disponibles para los
        # evaluadores
        available_dates_labels = [
            f"date-{date.label()}" for date in evaluators[0].available_dates
        ]
        for group in groups:
            assigned_date = assigned_dates[f"group-{group.id()}"]
            assert (
                assigned_date in available_dates_labels
            ), f"Group {group.id()} assigned date is not available for the evaluator."
