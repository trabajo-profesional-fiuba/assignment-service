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

    @pytest.mark.unit
    def test_groups_to_dates_edges(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)

        g1.add_avaliable_dates([self.dates[0], self.dates[1]])
        g2.add_avaliable_dates([self.dates[2]])
        g3.add_avaliable_dates([self.dates[3]])

        groups = [g1, g2, g3]
        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]
        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, [], [])
        expected_edges = [
            ("1", self.dates[0].label(), {
             "capacity": 1, "cost": 1}),
            ("1", self.dates[1].label(), {
             "capacity": 1, "cost": 1}),
            ("2", self.dates[2].label(), {
             "capacity": 1, "cost": 1}),
            ("3", self.dates[3].label(), {
             "capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_date_edges(groups, possible_dates)

        # Assert

        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_dates_to_sink_edges(self):
        # Arrange
        possible_dates = [self.dates[0], self.dates[1],
                          self.dates[2], self.dates[3]]
        delivery_flow_solver = DeliveryFlowSolver([], possible_dates, None, [], [])
        expected_edges = [
            (self.dates[0].label(), "t", {"capacity": 1, "cost": 1}),
            (self.dates[1].label(), "t", {"capacity": 1, "cost": 1}),
            (self.dates[2].label(), "t", {"capacity": 1, "cost": 1}),
            (self.dates[3].label(), "t", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_sink_edges(possible_dates, 1)

        # Assert

        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_group_graph(self):

        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)

        g1.add_avaliable_dates([self.dates[0], self.dates[1]])
        g2.add_avaliable_dates([self.dates[2]])
        g3.add_avaliable_dates([self.dates[3]])
        groups = [g1, g2, g3]
        possible_dates = [self.dates[0], self.dates[1],
                          self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        expected_edges = [
            ("s", "1"),
            ("s", "2"),
            ("s", "3"),
            ("1", self.dates[0].label()),
            ("1", self.dates[1].label()),
            ("2", self.dates[2].label()),
            ("3", self.dates[3].label()),
            (self.dates[0].label(), "t"),
            (self.dates[1].label(), "t"),
            (self.dates[2].label(), "t"),
            (self.dates[3].label(), "t"),
        ]
        # Act
        graph = delivery_flow_solver.groups_assigment_flow()

        #Assert
        assert all(graph.has_edge(e[0], e[1]) for e in expected_edges)

    @pytest.mark.unit
    def test_max_flow_min_cost(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)

        g1.add_avaliable_dates([self.dates[0]])
        g2.add_avaliable_dates([self.dates[1]])
        g3.add_avaliable_dates([self.dates[3]])
        groups = [g1, g2, g3]

        possible_dates = [self.dates[0], self.dates[1],
                          self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        graph = delivery_flow_solver.groups_assigment_flow()

        result = delivery_flow_solver._max_flow_min_cost(graph)

        assert result["1"][self.dates[0].label()] == 1
        assert result["2"][self.dates[1].label()] == 1
        assert result["3"][self.dates[3].label()] == 1


    @pytest.mark.unit
    def test_all_groups_have_one_day_assigned(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)
        g4 = Group(4, None)

        g1.add_avaliable_dates([self.dates[0]])
        g2.add_avaliable_dates([self.dates[1]])
        g3.add_avaliable_dates([self.dates[3]])
        g4.add_avaliable_dates([self.dates[2],self.dates[1]])

        groups = [g1, g2, g3, g4]

        possible_dates = [self.dates[0], self.dates[1],
                          self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        graph = delivery_flow_solver.groups_assigment_flow()

        result = delivery_flow_solver._max_flow_min_cost(graph)

        assert sum(result["1"].values()) == 1
        assert sum(result["2"].values()) == 1
        assert sum(result["3"].values()) == 1
        assert sum(result["4"].values()) == 1


    @pytest.mark.unit
    def test_evaluators_week_days_edges(self):
        # Arrange
        evaluators = [
            Evaluator(1, [self.dates[2], self.dates[3]]),
            Evaluator(2, [self.dates[1]]),
            Evaluator(3, [self.dates[0]]),
        ]
        delivery_flow_solver = DeliveryFlowSolver([], [],None,  [], [])

        expected_edges = [
            ("1", "2-1", {"capacity": 5, "cost": 1}),
            ("2-1", self.dates[2].label(),{"capacity": 1, "cost": 1}),
            ("2-1", self.dates[3].label(),{"capacity": 1, "cost": 1}),
            ("2", "1-2", {"capacity": 5, "cost": 1}),
            ("1-2", self.dates[1].label(),{"capacity": 1, "cost": 1}),
            ("3", "1-3", {"capacity": 5, "cost": 1}),
            ("1-3", self.dates[0].label(),{"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_evaluators_week_edges(evaluators)

        # Assert

        assert all(e in result for e in expected_edges)