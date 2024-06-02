import pytest

from src.algorithms.delivery_flow_solver import DeliveryFlowSolver
from src.model.group.base_group import Group
from src.model.utils.delivery_date import DeliveryDate


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
        g1 = Group(1)
        g2 = Group(2)
        groups = [g1, g2]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])
        expected_edges = [
            ("s", "1", {"capacity": 1, "cost": 1}),
            ("s", "2", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(groups, 1)

        # Assert
        assert all(e in result for e in expected_edges)
