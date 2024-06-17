import pytest
import networkx as nx
from src.assignments.date.delivery_flow_solver import DeliveryFlowSolver
from src.io.input_formatter import InputFormatter, get_evaluators
from src.io.output.output_formatter import OutputFormatter
from src.model.group.group import Group
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator
from src.model.tutor.tutor import Tutor
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
    def test_dates_to_sink_edges(self):
        # Arrange
        delivery_flow_solver = DeliveryFlowSolver([], [], None, [], [])
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
    def test_create_groups_edges(self, mocker):

        # Arrange
        group1 = Group(1)
        group1.add_available_dates([self.dates[0]])
        mocker.patch.object(group1, "filter_dates", return_value=None)
        mocker.patch.object(group1, "available_dates", return_value=[self.dates[0]])
        mocker.patch.object(group1, "cost_of_date", return_value=10)
        groups = [group1]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, [], [])
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
        tutor = Tutor(1, "fake@fi.uba.ar", "Jon Doe")
        mocker.patch.object(
            tutor,
            "available_dates",
            return_value=[self.dates[0], self.dates[1], self.dates[2]],
        )

        group1 = Group(1, tutor)
        group1.add_available_dates([self.dates[0]])

        group2 = Group(2, tutor)
        group2.add_available_dates([self.dates[1]])

        groups = [group1, group2]

        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, [], [])

        expected_edges = [self.dates[0].label(), self.dates[1].label()]

        # Act
        result = delivery_flow_solver._filter_groups_dates(mutual_dates)

        # Assert
        assert all(e in result for e in expected_edges)

    @pytest.mark.unit
    def test_mutual_dates_between_evaluators_and_group(self, mocker):
        # Arrange
        tutor = Tutor(1, "fake@fi.uba.ar", "Jon Doe")
        group1 = Group(1, tutor)
        group1.add_available_dates([self.dates[0], self.dates[1], self.dates[2]])
        groups = [group1]
        dates = [self.dates[0].label(), self.dates[1].label()]
        delivery_flow_solver = DeliveryFlowSolver(groups, [], None, [], [])

        # Act
        expected_groups = delivery_flow_solver._get_groups_id_with_mutual_dates(
            1, dates, 2
        )
        expected_cost = 5 * 11 - 2
        # Assert
        assert expected_groups[0][0] == 1
        assert expected_groups[0][1] == expected_cost

    @pytest.mark.unit
    def test_filter_evaluators_dates(self):
        # Arrange
        evaluator = Evaluator(
            1, available_dates=[self.dates[0], self.dates[1], self.dates[2]]
        )
        evaluators = [evaluator]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, self.dates, evaluators)
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
    def test_clean_evaluators_results(self):
        # Arrange
        evaluator = Evaluator(1, available_dates=[self.dates[0]])
        evaluators = [evaluator]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, self.dates, evaluators)
        evaluator_results = {
            f"{EVALUATOR_ID}-1": {f"{DATE_ID}-1-evaluator-1": 1},
            f"{DATE_ID}-1-evaluator-1": {"group-1": 1},
        }

        # Act
        result = delivery_flow_solver._clean_evaluators_results(evaluator_results)

        # Assert
        assert result["group-1"] == (1, 1)

    @pytest.mark.unit
    def test_get_evaluators_dates_by_id(self):
        # Arrange
        evaluator = Evaluator(
            1, available_dates=[self.dates[0], self.dates[1], self.dates[2]]
        )
        evaluators = [evaluator]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, self.dates, evaluators)
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
    def test_find_substitutes_for_group_on_date(self):
        # Arrange
        evaluator1 = Evaluator(
            1, available_dates=[self.dates[0], self.dates[1], self.dates[2]]
        )
        evaluator2 = Evaluator(2, available_dates=[self.dates[1], self.dates[2]])
        evaluators = [evaluator1, evaluator2]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, self.dates, evaluators)
        expected_substitutes = [evaluator2]

        # Act
        result = delivery_flow_solver._find_substitutes_on_date(
            self.dates[2].label(), 1
        )

        # Assert
        assert all(e in result for e in expected_substitutes)

    @pytest.mark.unit
    def test_evaluator_edges(self, mocker):
        # Arrange
        evaluator1 = Evaluator(1, available_dates=[self.dates[0], self.dates[1]])
        evaluators = [evaluator1]
        delivery_flow_solver = DeliveryFlowSolver([], [], None, self.dates, evaluators)
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
    def test_evaluator_valid_flow(self, mocker):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 3, 4), DeliveryDate(1, 1, 2)]
        tutor = Tutor(1, "fake@fi.uba.ar", "Jon Doe")
        group1 = Group(1, tutor)
        group1.add_available_dates([dates[0], dates[1]])
        group2 = Group(2, tutor)
        group2.add_available_dates([dates[2]])
        evaluator = Evaluator(3, dates)
        delivery_flow_solver = DeliveryFlowSolver(
            [group1, group2], [tutor], None, dates, [evaluator]
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
    def test_complete_valid_flow(self, mocker):
        # Arrange
        dates = [DeliveryDate(1, 2, 3), DeliveryDate(1, 3, 4), DeliveryDate(1, 1, 2)]
        tutor = Tutor(1, "fake@fi.uba.ar", "Jon Doe")
        mocker.patch.object(tutor, 'available_dates', return_value=dates)
        group1 = Group(1, tutor)
        group1.add_available_dates([dates[0], dates[1]])
        group2 = Group(2, tutor)
        group2.add_available_dates([dates[2]])
        groups = [group1, group2]
        evaluator = Evaluator(2, dates)
        delivery_flow_solver = DeliveryFlowSolver(
            groups, [tutor], None, dates, [evaluator]
        )

        # Act
        max_flow_min_cost = delivery_flow_solver.solve()

        # Assertion
        assert len(max_flow_min_cost["s"].keys()) == 2
        for k,v in max_flow_min_cost["s"].items():
            assert v == 1
        
        

    # @pytest.mark.unit
    @pytest.mark.skip(reason="Todavia hay que ajustar el codigo")
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
        # Check that there are three evaluators
        evaluators_id = []
        for tutor in tutors:
            if tutor.name in get_evaluators():
                evaluators_id.append(tutor.id)
        assert len(evaluators) == 3

        # Check that expected evaluators were created
        evaluators_count = {evaluator.id: 0 for evaluator in evaluators}
        for evaluator in evaluators:
            for id in evaluators_id:
                if evaluator.id == id:
                    evaluators_count[evaluator.id] += 1
        for evaluator, count in evaluators_count.items():
            assert count == 1

        flow_solver = DeliveryFlowSolver(
            groups, tutors, OutputFormatter(), possible_dates, evaluators
        )

        result = flow_solver.solve()

        # Check that all groups are in result
        groups_result = result.groups
        assert len(groups_result) == len(groups)
        for group in groups_result:
            # Check that all groups have an assigned date set
            assert result.delivery_date_group(group) is not None
            # Check that assigned date is in group available dates
            group_available_dates = []
            for available_date in group.available_dates():
                group_available_dates.append(f"date-{available_date.label()}")
            assert result.delivery_date_group(group) in group_available_dates
            print(
                f"group {group.id}, tutor {group.tutor.id}, delivery_date\
                {result.delivery_date_group(group)}"
            )

        # Check that all evaluators are in result
        evaluators_result = result.evaluators
        for evaluator in evaluators_result:
            print(
                f"evaluator {evaluator.id}, count delivery_date\
                {len(result.delivery_date_evaluator(evaluator))}"
            )
            for assigned_date in result.delivery_date_evaluator(evaluator):
                print(f"evaluator {evaluator.id}, delivery_date {assigned_date}")
                # Check that assigned date is in evaluator available dates
                available_dates = []
                for available_date in evaluator.available_dates:
                    available_dates.append(f"date-{available_date.label()}")
                assert assigned_date in available_dates

        # Check that evaluators are not assigned dates that were assigned to groups
        # they are tutoring
        for group in groups_result:
            for evaluator in evaluators_result:
                if evaluator.id == group.tutor.id:
                    print(
                        f"group {group.id}, tutor {group.tutor.name}\
                    {group.tutor.id}, evaluator {evaluator.id}"
                    )
                    for assigned_date in result.delivery_date_evaluator(evaluator):
                        assert assigned_date != result.delivery_date_group(group)
