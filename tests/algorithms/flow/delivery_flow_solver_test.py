import pytest

from src.algorithms.delivery_flow_solver import DeliveryFlowSolver
from src.model.group.base_group import Group
from src.model.group.final_state_group import FinalStateGroup
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evalutor import Evaluator



class TestDeliveryFlowSolver:
    dates = [
        DeliveryDate(week=1, day=1, hour=1),
        DeliveryDate(week=1, day=2, hour=1),
        DeliveryDate(week=2, day=1, hour=1),
        DeliveryDate(week=2, day=2, hour=1)
    ]

    @pytest.mark.unit
    def test_source_to_groups_edges(self):

        # Arrange
        groups = [
            Group(1),
            Group(2)
        ]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])
        expected_edges = [
            ("s", "1", {"capacity": 1, "cost": 1}),
            ("s", "2", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(groups, 1)

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
            ("s", "1", {"capacity": 35, "cost": 1}),
            ("s", "2", {"capacity": 35, "cost": 1}),
            ("s", "3", {"capacity": 35, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(evaluators, 35)

        # Assert

        assert all(e in result for e in expected_edges)
