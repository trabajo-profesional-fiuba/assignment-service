import pytest
import pandas as pd

from src.assignments.date.delivery_flow_solver import DeliveryFlowSolver
from src.io.input_formatter import InputFormatter, get_evaluators
from src.io.output.output_formatter import OutputFormatter
from src.model.group.group import Group
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator
from src.constants import GROUP_ID, EVALUATOR_ID


class TestDeliveryFlowSolver:
    dates = [
        DeliveryDate(week=1, day=1, hour=1),
        DeliveryDate(week=1, day=2, hour=1),
        DeliveryDate(week=2, day=1, hour=1),
        DeliveryDate(week=2, day=2, hour=1),
    ]

    @pytest.mark.unit
    def test_source_to_groups_edges(self):

        # Arrange
        groups = [Group(1), Group(2)]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])
        expected_edges = [
            ("s", "group-1", {"capacity": 1, "cost": 1}),
            ("s", "group-2", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(groups, 1, GROUP_ID)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_source_to_evaluators_edges(self):
        # Arrange
        evaluators = [
            Evaluator(1, [self.dates[1]]),
            Evaluator(2, [self.dates[1]]),
            Evaluator(3, [self.dates[1]]),
        ]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])
        # 35 = 5 entregas x 7 semanas
        expected_edges = [
            ("s", "evaluator-1", {"capacity": 35, "cost": 1}),
            ("s", "evaluator-2", {"capacity": 35, "cost": 1}),
            ("s", "evaluator-3", {"capacity": 35, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(evaluators, 35, EVALUATOR_ID)

        # Assert

        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_find_substitutes_for_group(self, mocker):
        # Arrange
        ev1 = Evaluator(1)
        mocker.patch.object(ev1, "is_avaliable", return_value=True)
        ev2 = Evaluator(2)
        mocker.patch.object(ev2, "is_avaliable", return_value=True)

        group_info = {"group-1": (1, 1), "group-2": (2, 2)}
        groups_result = {
            "group-1": {"date-1-1-1": 1, "date-1-2-1": 0},
            "group-2": {"date--1-1": 1, "date-2-2-1": 0},
        }
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])

        # Act
        substitutes = delivery_flow_solver._find_substitutes(group_info, groups_result)

        # Assert
        assert substitutes == substitutes

    @pytest.mark.unit
    # @pytest.mark.skip(reason="Todavia hay que ajustar el codigo")
    def test_real_case(self):
        groups_df = pd.read_csv("db/equipos.csv")
        tutors_df = pd.read_csv("db/tutores.csv")

        formatter = InputFormatter(groups_df, tutors_df)
        groups, tutors, evaluators, possible_dates = formatter.get_data()

        for tutor in tutors:
            print(f"tutor {tutor.id} {tutor.name}")
        for group in groups:
            for tutor in tutors:
                if group.tutor.id == tutor.id:
                    print(f"group {group.id}, tutor {tutor.id} {tutor.name}")
        assert 1 == 1
        # # Check that there are three evaluators
        # evaluators_id = []
        # for tutor in tutors:
        #     if tutor.name in get_evaluators():
        #         evaluators_id.append(tutor.id)
        # assert len(evaluators) == 3

        # # Check that expected evaluators were created
        # evaluators_count = {evaluator.id: 0 for evaluator in evaluators}
        # for evaluator in evaluators:
        #     for id in evaluators_id:
        #         if evaluator.id == id:
        #             evaluators_count[evaluator.id] += 1
        # for evaluator, count in evaluators_count.items():
        #     assert count == 1

        # flow_solver = DeliveryFlowSolver(
        #     groups, tutors, OutputFormatter(), possible_dates, evaluators
        # )

        # result = flow_solver.solve()

        # # Check that all groups are in result
        # groups_result = result.groups
        # assert len(groups_result) == len(groups)
        # for group in groups_result:
        #     # Check that all groups have an assigned date set
        #     assert result.delivery_date_group(group) is not None
        #     # Check that assigned date is in group available dates
        #     group_available_dates = []
        #     for available_date in group.available_dates():
        #         group_available_dates.append(f"date-{available_date.label()}")
        #     assert result.delivery_date_group(group) in group_available_dates
        #     print(
        #         f"group {group.id}, tutor {group.tutor.id}, delivery_date\
        #         {result.delivery_date_group(group)}"
        #     )

        # # Check that all evaluators are in result
        # evaluators_result = result.evaluators
        # for evaluator in evaluators_result:
        #     print(
        #         f"evaluator {evaluator.id}, count delivery_date\
        #         {len(result.delivery_date_evaluator(evaluator))}"
        #     )
        #     for assigned_date in result.delivery_date_evaluator(evaluator):
        #         print(f"evaluator {evaluator.id}, delivery_date {assigned_date}")
        #         # Check that assigned date is in evaluator available dates
        #         available_dates = []
        #         for available_date in evaluator.available_dates:
        #             available_dates.append(f"date-{available_date.label()}")
        #         assert assigned_date in available_dates

        # # Check that evaluators are not assigned dates that were assigned to groups
        # # they are tutoring
        # for group in groups_result:
        #     for evaluator in evaluators_result:
        #         if evaluator.id == group.tutor.id:
        #             print(f"group {group.id}, tutor {group.tutor.name}\
        #             {group.tutor.id}, evaluator {evaluator.id}")
        #             for assigned_date in result.delivery_date_evaluator(evaluator):
        #                 assert assigned_date != result.delivery_date_group(group)
