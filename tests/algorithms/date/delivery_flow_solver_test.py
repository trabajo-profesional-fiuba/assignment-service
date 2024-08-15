import pytest
import networkx as nx
from src.core.algorithms.date.delivery_flow_solver import DeliveryFlowSolver
from src.core.algorithms.adapters.result_adapter import ResultAdapter
from src.core.group import Group
from src.core.delivery_date import DeliveryDate
from src.core.tutor import Tutor
from src.core.period import TutorPeriod
from src.constants import GROUP_ID, EVALUATOR_ID, DATE_ID
from src.core.algorithms.exceptions import AssigmentIsNotPossible


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
        delivery_flow_solver = DeliveryFlowSolver()
        expected_edges = [
            ("s", "group-1", {"capacity": 1, "cost": 1}),
            ("s", "group-2", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(groups, 1, GROUP_ID)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_dates_to_sink_edges(self):
        # Arrange
        delivery_flow_solver = DeliveryFlowSolver()

        # 35 = 5 entregas x 7 semanas
        expected_edges = [
            (f"date-{self.dates[0].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"date-{self.dates[1].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"date-{self.dates[2].label()}", "t", {"capacity": 1, "cost": 1}),
            (f"date-{self.dates[3].label()}", "t", {"capacity": 1, "cost": 1}),
        ]
        dates = [d.label() for d in self.dates]

        # Act
        result = delivery_flow_solver._create_sink_edges(dates, 1, DATE_ID)

        # Assert

        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_source_to_evaluators_edges(self, mocker):
        # Arrange
        period1 = TutorPeriod(period="1C2024")
        mocker.patch.object(period1, "id", return_value=1)
        period2 = TutorPeriod(period="1C2024")
        mocker.patch.object(period2, "id", return_value=2)

        delivery_flow_solver = DeliveryFlowSolver()
        # 35 = 5 entregas x 7 semanas
        expected_edges = [
            ("s", "evaluator-1", {"capacity": 35, "cost": 1}),
            ("s", "evaluator-2", {"capacity": 35, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_source_edges(
            [period1, period2], 35, EVALUATOR_ID
        )

        # Assert

        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_create_groups_edges(self, mocker):

        # Arrange
        group1 = Group(1)
        group1.add_available_dates([self.dates[0]])
        mocker.patch.object(group1, "filter_dates", return_value=None)
        mocker.patch.object(group1, "cost_of_date", return_value=10)
        groups = [group1]
        period = TutorPeriod(period="1C2024")
        period.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(tutor_periods=[period])
        mocker.patch.object(
            delivery_flow_solver, "_get_evaluator_dates", return_value=[self.dates[0]]
        )

        clean_results = {"group-1": (1, 1)}
        expected_edges = [
            ("s", "group-1", {"capacity": 1, "cost": 1}),
            (
                "group-1",
                f"{DATE_ID}-{self.dates[0].label()}",
                {"capacity": 1, "cost": 10},
            ),
            (f"{DATE_ID}-{self.dates[0].label()}", "t", {"capacity": 1, "cost": 1}),
        ]

        # Act
        result = delivery_flow_solver._create_group_date_edges(clean_results)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_filter_group_dates(self, mocker):
        # Arrange
        mutual_dates = [
            self.dates[0].label(),
            self.dates[1].label(),
            self.dates[2].label(),
        ]

        group1 = Group(1)
        group1.add_available_dates([self.dates[0]])

        group2 = Group(2)
        group2.add_available_dates([self.dates[1]])

        groups = [group1, group2]
        period = TutorPeriod(period="1C2024")
        period.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(tutor_periods=[period])

        expected_edges = [self.dates[0].label(), self.dates[1].label()]

        # Act
        result = delivery_flow_solver._filter_groups_dates(mutual_dates)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_mutual_dates_between_evaluators_and_group(self, mocker):
        # Arrange
        group1 = Group(1)
        group1.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        groups = [group1]
        dates = [self.dates[0].label(), self.dates[1].label()]
        period = TutorPeriod(period="1C2024")
        period.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(tutor_periods=[period])

        # Act
        expected_groups = delivery_flow_solver._get_groups_id_with_mutual_dates(
            1, dates, [2]
        )
        expected_cost = 5 * 11 - 2
        # Assert
        assert expected_groups[0][0] == 1
        assert expected_groups[0][1] == expected_cost

    @pytest.mark.unit
    def test_filter_evaluators_dates(self):

        # Arrange
        period = TutorPeriod(period="1C2024")
        period.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        period.make_evaluator()

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period], available_dates=self.dates
        )
        expected_dates = [
            self.dates[0].label(),
            self.dates[1].label(),
            self.dates[2].label(),
        ]

        # Act
        result = delivery_flow_solver._filter_evaluators_dates()

        # Assert
        assert all(e in result for e in expected_dates)

    @pytest.mark.unit
    def test_clean_evaluators_results(self, mocker):
        # Arrange
        period = TutorPeriod(period="1C2024")
        mocker.patch.object(period, "id", return_value=1)
        period.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        period.make_evaluator()

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period], available_dates=self.dates
        )

        evaluator_results = {
            f"{EVALUATOR_ID}-1": {f"{DATE_ID}-1-evaluator-1": 1},
            f"{DATE_ID}-1-evaluator-1": {"group-1": 1},
        }

        # Act
        result = delivery_flow_solver._clean_evaluators_results(evaluator_results)

        # Assert
        assert result["group-1"] == (1, 1)

    @pytest.mark.unit
    def test_get_evaluators_dates_by_id(self, mocker):
        # Arrange
        period = TutorPeriod(period="1C2024")
        mocker.patch.object(period, "id", return_value=1)
        period.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        period.make_evaluator()

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period], available_dates=self.dates
        )
        expected_dates = [
            self.dates[0].label(),
            self.dates[1].label(),
            self.dates[2].label(),
        ]

        # Act
        result = delivery_flow_solver._get_evaluator_dates(1)

        # Assert
        assert all(e in result for e in expected_dates)

    @pytest.mark.unit
    def test_find_substitutes_for_group_on_date(self, mocker):
        # Arrange
        period1 = TutorPeriod(period="1C2024")
        mocker.patch.object(period1, "id", return_value=1)
        period1.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        period1.make_evaluator()

        period2 = TutorPeriod(period="1C2024")
        mocker.patch.object(period2, "id", return_value=2)
        period2.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        period2.make_evaluator()

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period1, period2], available_dates=self.dates
        )
        expected_substitutes = [period2]

        # Act
        result = delivery_flow_solver._find_substitutes_on_date(
            self.dates[2].label(), 1
        )

        # Assert
        assert all(e in result for e in expected_substitutes)

    @pytest.mark.unit
    def test_evaluator_edges(self, mocker):
        # Arrange
        period1 = TutorPeriod(period="1C2024")
        mocker.patch.object(period1, "id", return_value=1)
        period1.add_available_dates([self.dates[0], self.dates[1]])
        period1.make_evaluator()
        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period1], available_dates=self.dates
        )

        mocker.patch.object(
            delivery_flow_solver,
            "_get_groups_id_with_mutual_dates",
            return_value=[(1, 10)],
        )
        expected_edges = [
            ("s", f"{EVALUATOR_ID}-1", {"capacity": 35, "cost": 1}),
            (
                f"{EVALUATOR_ID}-1",
                f"{DATE_ID}-1-{EVALUATOR_ID}-1",
                {"capacity": 5, "cost": 1},
            ),
            (
                f"{DATE_ID}-1-{EVALUATOR_ID}-1",
                f"{GROUP_ID}-1",
                {"capacity": 1, "cost": 10},
            ),
            (f"{GROUP_ID}-1", "t", {"capacity": 1, "cost": 1}),
        ]
        # Act
        result = delivery_flow_solver._create_evaluators_edges()

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_find_substitutes_for_group(self, mocker):
        # Arrange
        period1 = TutorPeriod(period="1C2024")
        period1.make_evaluator()
        mocker.patch.object(period1, "id", return_value=1)
        mocker.patch.object(period1, "is_avaliable", return_value=True)

        period2 = TutorPeriod(period="1C2024")
        period2.make_evaluator()
        mocker.patch.object(period2, "id", return_value=2)
        mocker.patch.object(period2, "is_avaliable", return_value=True)

        group_info = {"group-1": (1, 1), "group-2": (2, 2)}
        groups_result = {
            "group-1": {"date-1-1-1": 1, "date-1-2-1": 0},
            "group-2": {"date-1-1-1": 0, "date-2-2-1": 1},
        }
        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period1, period2], available_dates=self.dates
        )

        # Act
        substitutes = delivery_flow_solver._find_substitutes(group_info, groups_result)

        # Assert
        assert substitutes["group-1"][0] == period2
        assert substitutes["group-2"][0] == period1

    @pytest.mark.unit
    def test_evaluator_valid_flow(self, mocker):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 3, 4), DeliveryDate(1, 1, 2)]
        group1 = Group(1)
        group1.add_available_dates([dates[0], dates[1]])
        group2 = Group(2)
        group2.add_available_dates([dates[2]])

        period = TutorPeriod(period="1C2024")
        period.make_evaluator()
        period.add_available_dates(dates)
        mocker.patch.object(period, "id", return_value=3)

        period2 = TutorPeriod(period="1C2024")
        mocker.patch.object(period2, "id", return_value=2)
        period2.add_groups([group1, group2])

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period, period2], available_dates=dates
        )

        evaluator_edges = delivery_flow_solver._create_evaluators_edges()
        e_graph = nx.DiGraph()
        e_graph.add_edges_from(evaluator_edges)

        # Act
        max_flow_min_cost_evaluator = delivery_flow_solver._max_flow_min_cost(e_graph)
        clean_results = delivery_flow_solver._clean_evaluators_results(
            max_flow_min_cost_evaluator
        )
        result = delivery_flow_solver._valid_evaluator_results(clean_results)

        # Assertion
        assert result is True

    @pytest.mark.unit
    def test_complete_valid_flow(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 3, 4), DeliveryDate(1, 1, 2)]

        adapter = ResultAdapter()

        group1 = Group(1)
        group1.add_available_dates([dates[0], dates[1]])
        group2 = Group(2)
        group2.add_available_dates([dates[2]])
        groups = [group1, group2]

        period = TutorPeriod(period="1C2024")
        period.make_evaluator()
        period.add_available_dates(dates)
        period.add_parent(Tutor(1, "f@fi.uba.ar", "Juan"))

        period2 = TutorPeriod(period="1C2024")
        period2.add_parent(Tutor(2, "f@fi.uba.ar", "Pepe"))
        period2.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period, period2], available_dates=dates, adapter=adapter
        )

        # Act
        result = delivery_flow_solver.solve()

        # Assertion
        assert len(result.get_results()) == 2

    @pytest.mark.unit
    def test_some_groups_does_not_contains_evaluators(self):
        group1 = Group(1)
        group2 = Group(2)
        period = TutorPeriod(period="1C2024")
        period.add_groups([group1, group2])
        delivery_flow_solver = DeliveryFlowSolver([period])

        group_info = {"group-1": (1, 1)}

        result = delivery_flow_solver._valid_evaluator_results(group_info)

        assert result is False

    @pytest.mark.unit
    def test_some_groups_does_not_contains_dates_assigned(self):
        group1 = Group(1)
        group2 = Group(2)
        period = TutorPeriod(period="1C2024")
        period.add_groups([group1, group2])
        delivery_flow_solver = DeliveryFlowSolver([period])

        groups_result = {
            "group-1": {"date-1-1-1": 1, "date-1-2-1": 0},
            "group-2": {"date-1-1-1": 0, "date-2-2-1": 0},
        }

        result = delivery_flow_solver._valid_groups_result(groups_result)

        assert result is False

    @pytest.mark.unit
    def test_group_without_date_raises_error(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3)]

        adapter = ResultAdapter()

        group1 = Group(1)
        group1.add_available_dates([dates[0]])
        group2 = Group(2)
        group2.add_available_dates([dates[0]])
        groups = [group1, group2]

        period = TutorPeriod(period="1C2024")
        period.make_evaluator()
        period.add_available_dates(dates)
        period.add_parent(Tutor(1, "f@fi.uba.ar", "Juan"))

        period2 = TutorPeriod(period="1C2024")
        period2.add_parent(Tutor(2, "f@fi.uba.ar", "Pepe"))
        period2.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period, period2], available_dates=dates, adapter=adapter
        )

        # Act & Assert
        with pytest.raises(
            AssigmentIsNotPossible, match="There are groups without assigned dates"
        ):
            delivery_flow_solver.solve()

    @pytest.mark.unit
    def test_group_without_evaluator_raises_error(self):
        # Arrange
        dates = [DeliveryDate(1, 2, 3)]

        adapter = ResultAdapter()

        group1 = Group(1)
        group1.add_available_dates([dates[0]])
        group2 = Group(2)
        groups = [group1, group2]

        period = TutorPeriod(period="1C2024")
        period.make_evaluator()
        period.add_available_dates(dates)
        period.add_parent(Tutor(1, "f@fi.uba.ar", "Juan"))

        period2 = TutorPeriod(period="1C2024")
        period2.add_parent(Tutor(2, "f@fi.uba.ar", "Pepe"))
        period2.add_groups(groups)

        delivery_flow_solver = DeliveryFlowSolver(
            tutor_periods=[period, period2], available_dates=dates, adapter=adapter
        )

        # Act & Assert
        with pytest.raises(
            AssigmentIsNotPossible, match="There are groups without avaliable evaluator"
        ):
            delivery_flow_solver.solve()
