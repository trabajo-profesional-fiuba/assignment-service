import pytest

from src.algorithms.delivery_flow_solver import DeliveryFlowSolver
from src.model.group.group import Group
from src.model.tutor.tutor import Tutor
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator
from src.constants import GROUP_ID, EVALUATOR_ID, DATE_ID


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
    def test_groups_to_dates_edges(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)

        g1.add_available_dates([self.dates[0], self.dates[1]])
        g2.add_available_dates([self.dates[2]])
        g3.add_available_dates([self.dates[3]])

        groups = [g1, g2, g3]
        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]
        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, [], [])
        expected_edges = [
            (
                "group-1",
                f"{DATE_ID}-{self.dates[0].label()}",
                {"capacity": 1, "cost": 1},
            ),
            (
                "group-1",
                f"{DATE_ID}-{self.dates[1].label()}",
                {"capacity": 1, "cost": 1},
            ),
            (
                "group-2",
                f"{DATE_ID}-{self.dates[2].label()}",
                {"capacity": 1, "cost": 1},
            ),
            (
                "group-3",
                f"{DATE_ID}-{self.dates[3].label()}",
                {"capacity": 1, "cost": 1},
            ),
        ]

        # Act
        result = delivery_flow_solver._create_date_edges(
            groups, possible_dates, GROUP_ID
        )

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_dates_to_sink_edges(self):
        # Arrange
        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]
        delivery_flow_solver = DeliveryFlowSolver([], possible_dates, None, [], [])
        expected_edges = [
            (f"{DATE_ID}-{self.dates[0].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"{DATE_ID}-{self.dates[1].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"{DATE_ID}-{self.dates[2].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"{DATE_ID}-{self.dates[3].label()}", "t", {"capacity": 1, "cost": 1}),
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

        g1.add_available_dates([self.dates[0], self.dates[1]])
        g2.add_available_dates([self.dates[2]])
        g3.add_available_dates([self.dates[3]])
        groups = [g1, g2, g3]
        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        expected_edges = [
            ("s", "group-1"),
            ("s", "group-2"),
            ("s", "group-3"),
            ("group-1", f"{DATE_ID}-{self.dates[0].label()}"),
            ("group-1", f"{DATE_ID}-{self.dates[1].label()}"),
            ("group-2", f"{DATE_ID}-{self.dates[2].label()}"),
            ("group-3", f"{DATE_ID}-{self.dates[3].label()}"),
            (f"{DATE_ID}-{self.dates[0].label()}", "t"),
            (f"{DATE_ID}-{self.dates[1].label()}", "t"),
            (f"{DATE_ID}-{self.dates[2].label()}", "t"),
            (f"{DATE_ID}-{self.dates[3].label()}", "t"),
        ]
        # Act
        graph = delivery_flow_solver.groups_assignment_flow()

        # Assert
        assert all(graph.has_edge(e[0], e[1]) for e in expected_edges)

    @pytest.mark.unit
    def test_max_flow_min_cost(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)

        g1.add_available_dates([self.dates[0]])
        g2.add_available_dates([self.dates[1]])
        g3.add_available_dates([self.dates[3]])
        groups = [g1, g2, g3]

        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        graph = delivery_flow_solver.groups_assignment_flow()

        result = delivery_flow_solver._max_flow_min_cost(graph)

        assert result["group-1"][f"{DATE_ID}-{self.dates[0].label()}"] == 1
        assert result["group-2"][f"{DATE_ID}-{self.dates[1].label()}"] == 1
        assert result["group-3"][f"{DATE_ID}-{self.dates[3].label()}"] == 1

    @pytest.mark.unit
    def test_all_groups_have_one_day_assigned(self):
        # Arrange
        g1 = Group(1, None)
        g2 = Group(2, None)
        g3 = Group(3, None)
        g4 = Group(4, None)

        g1.add_available_dates([self.dates[0]])
        g2.add_available_dates([self.dates[1]])
        g3.add_available_dates([self.dates[3]])
        g4.add_available_dates([self.dates[2], self.dates[1]])

        groups = [g1, g2, g3, g4]

        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, possible_dates, [])
        graph = delivery_flow_solver.groups_assignment_flow()

        result = delivery_flow_solver._max_flow_min_cost(graph)

        assert sum(result["group-1"].values()) == 1
        assert sum(result["group-2"].values()) == 1
        assert sum(result["group-3"].values()) == 1
        assert sum(result["group-4"].values()) == 1

    @pytest.mark.unit
    def test_evaluators_week_days_edges(self):
        # Arrange
        evaluators = [
            Evaluator(1, [self.dates[2], self.dates[3]]),
            Evaluator(2, [self.dates[1]]),
            Evaluator(3, [self.dates[0]]),
        ]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])

        expected_edges = [
            ("evaluator-1", f"{DATE_ID}-2-evaluator-1", {"capacity": 5, "cost": 1}),
            (
                f"{DATE_ID}-2-evaluator-1",
                f"{DATE_ID}-{self.dates[2].label()}",
                {"capacity": 1, "cost": 1},
            ),
            (
                f"{DATE_ID}-2-evaluator-1",
                f"{DATE_ID}-{self.dates[3].label()}",
                {"capacity": 1, "cost": 1},
            ),
            ("evaluator-2", f"{DATE_ID}-1-evaluator-2", {"capacity": 5, "cost": 1}),
            (
                f"{DATE_ID}-1-evaluator-2",
                f"{DATE_ID}-{self.dates[1].label()}",
                {"capacity": 1, "cost": 1},
            ),
            ("evaluator-3", f"{DATE_ID}-1-evaluator-3", {"capacity": 5, "cost": 1}),
            (
                f"{DATE_ID}-1-evaluator-3",
                f"{DATE_ID}-{self.dates[0].label()}",
                {"capacity": 1, "cost": 1},
            ),
        ]

        # Act
        result = delivery_flow_solver._create_evaluators_week_edges(evaluators)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_dates_to_sink_with_capacity_edges(self):
        # Arrange
        possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, possible_dates, [])

        expected_edges = [
            (f"{DATE_ID}-{self.dates[0].label()}", "t", {"capacity": 2, "cost": 1}),
            (f"{DATE_ID}-{self.dates[1].label()}", "t", {"capacity": 2, "cost": 1}),
            (f"{DATE_ID}-{self.dates[2].label()}", "t", {"capacity": 2, "cost": 1}),
            (f"{DATE_ID}-{self.dates[3].label()}", "t", {"capacity": 2, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_sink_edges(possible_dates, 2)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_evaluator_graph(self):
        # Arrange

        dates = [
            DeliveryDate(week=1, day=1, hour=1),
            DeliveryDate(week=1, day=2, hour=1),
            DeliveryDate(week=2, day=1, hour=1),
            DeliveryDate(week=2, day=2, hour=1),
            DeliveryDate(week=3, day=1, hour=1),
            DeliveryDate(week=3, day=2, hour=1),
            DeliveryDate(week=4, day=1, hour=2),
            DeliveryDate(week=4, day=2, hour=2),
        ]

        # e1 puede : 1-1-1, 1-2-1, 2-1-1, 2-2-1
        # e2 puede : 2-1-1, 2-2-1, 3-1-1, 3-2-1
        # e3 puede:  4-1-2, 4-2-2
        evaluators = [
            Evaluator(1, [dates[0], dates[1], dates[2], dates[3]]),
            Evaluator(2, [dates[2], dates[3], dates[4], dates[5]]),
            Evaluator(3, [dates[6], dates[7]]),
        ]

        delivery_flow_solver = DeliveryFlowSolver([], [], None, dates, evaluators)

        expected_edges = [
            ("s", "evaluator-1"),
            ("s", "evaluator-2"),
            ("s", "evaluator-3"),
            ("evaluator-1", f"{DATE_ID}-1-evaluator-1"),
            ("evaluator-1", f"{DATE_ID}-2-evaluator-1"),
            (f"{DATE_ID}-1-evaluator-1", f"{DATE_ID}-1-1-1"),
            (f"{DATE_ID}-1-evaluator-1", f"{DATE_ID}-1-2-1"),
            (f"{DATE_ID}-2-evaluator-1", f"{DATE_ID}-2-1-1"),
            (f"{DATE_ID}-2-evaluator-1", f"{DATE_ID}-2-2-1"),
            ("evaluator-2", f"{DATE_ID}-2-evaluator-2"),
            ("evaluator-2", f"{DATE_ID}-3-evaluator-2"),
            (f"{DATE_ID}-2-evaluator-2", f"{DATE_ID}-2-1-1"),
            (f"{DATE_ID}-2-evaluator-2", f"{DATE_ID}-2-2-1"),
            (f"{DATE_ID}-3-evaluator-2", f"{DATE_ID}-3-1-1"),
            (f"{DATE_ID}-3-evaluator-2", f"{DATE_ID}-3-2-1"),
            ("evaluator-3", f"{DATE_ID}-4-evaluator-3"),
            (f"{DATE_ID}-4-evaluator-3", f"{DATE_ID}-4-1-2"),
            (f"{DATE_ID}-4-evaluator-3", f"{DATE_ID}-4-2-2"),
            (f"{DATE_ID}-{dates[0].label()}", "t"),
            (f"{DATE_ID}-{dates[1].label()}", "t"),
            (f"{DATE_ID}-{dates[2].label()}", "t"),
            (f"{DATE_ID}-{dates[3].label()}", "t"),
            (f"{DATE_ID}-{dates[4].label()}", "t"),
            (f"{DATE_ID}-{dates[5].label()}", "t"),
        ]

        # Act
        graph = delivery_flow_solver.evaluators_assignment_flow()

        assert all(graph.has_edge(e[0], e[1]) for e in expected_edges)

    @pytest.mark.unit
    def test_assign_evaluators_dates(self):
        dates = [
            DeliveryDate(week=1, day=1, hour=1),
            DeliveryDate(week=1, day=2, hour=1),
            DeliveryDate(week=2, day=1, hour=1),
            DeliveryDate(week=2, day=2, hour=1),
            DeliveryDate(week=3, day=1, hour=1),
            DeliveryDate(week=3, day=2, hour=1),
        ]
        result = {
            "evaluator-1": {
                "date-1-evaluator-1": 2,
                "date-2-evaluator-1": 2,
                "date-3-evaluator-1": 0
            },
            "date-1-evaluator-1": {
                "date-1-1-1-1": 1,
                "date-1-1-2-1": 1
            },
            "date-2-evaluator-1": {
                "date-2-2-1-1": 1,
                "date-2-2-2-1": 1
            },
            "date-1-1-1-1": {
                "t": 1
            },
            "date-1-1-2-1": {
                "t": 1
            },
            "date-2-2-1-1": {
                "t": 1
            },
            "date-2-2-2-1": {
                "t": 1
            }
        }

        evaluators = [
            Evaluator(1, [dates[0], dates[1], dates[2], dates[3],dates[4],dates[5]])
        ]

        delivery_flow_solver = DeliveryFlowSolver([], [], None, dates, evaluators)
        delivery_flow_solver._assign_evaluators_results(result)
        assert len(evaluators[0].assigned_dates) == 4

    @pytest.mark.unit
    def test_small_use_case(self):
        g1 = Group(1, Tutor(2, "fake@fi.uba.com", "Juan", state=FinalStateTutor()))
        g2 = Group(2, Tutor(1, "fak3@fi.uba.com", "Pedro", state=FinalStateTutor()))
        """
        DeliveryDate(week=1, day=1, hour=1),
        DeliveryDate(week=1, day=2, hour=1),
        DeliveryDate(week=2, day=1, hour=1),
        DeliveryDate(week=2, day=2, hour=1)
        """

        g1.add_available_dates([self.dates[0], self.dates[1]])
        g2.add_available_dates([self.dates[2], self.dates[3]])

        # possible_dates = [self.dates[0], self.dates[1], self.dates[2], self.dates[3]]
        # evaluators = [
        #     Evaluator(1, [self.dates[2]]),
        #     Evaluator(2, [self.dates[1]]),
        #     Evaluator(3, [self.dates[0]]),
        #     Evaluator(4, [self.dates[2], self.dates[3]]),
        # ]
        # assert 1 == 1
