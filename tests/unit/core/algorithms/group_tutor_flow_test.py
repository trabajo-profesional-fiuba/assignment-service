import pytest

from src.core.algorithms.topic_tutor.group_tutor_flow_solver import GroupTutorFlowSolver
from src.core.group import UnassignedGroup
from src.core.topic import Topic
from src.core.tutor import Tutor


class TestGroupTutorFlowSolver:

    @pytest.mark.unit
    def test_create_source_group_edges(self):
        groups = [
            UnassignedGroup(
                1,
                topics=[],
                students=[],
            ),
            UnassignedGroup(
                2,
                topics=[],
                students=[],
            ),
        ]
        solver = GroupTutorFlowSolver(groups=groups)
        edges = solver._create_source_groups_edges()
        assert len(edges) == 2

    @pytest.mark.unit
    def test_create_topic_group_edges(self):
        topics = [
            Topic(id=0, title="Tema C", capacity=10, category="Category A"),
            Topic(id=1, title="Tema A", capacity=10, category="Category A"),
            Topic(id=2, title="Tema B", capacity=10, category="Category A"),
            Topic(id=3, title="Tema E", capacity=10, category="Category B"),
        ]

        groups = [
            UnassignedGroup(
                1,
                topics=[topics[0], topics[1], topics[2]],
                students=[],
            ),
            UnassignedGroup(
                2,
                topics=[topics[1], topics[2], topics[3]],
                students=[],
            ),
        ]
        solver = GroupTutorFlowSolver(groups=groups, topics=topics)
        edges = solver._create_groups_topics_edges()
        assert len(edges) == 8

    @pytest.mark.unit
    def test_create_tutor_topics_edges(self):
        topics = [
            Topic(id=0, title="Tema C", capacity=10, category="Category A"),
            Topic(id=1, title="Tema A", capacity=10, category="Category A"),
            Topic(id=2, title="Tema B", capacity=10, category="Category A"),
            Topic(id=3, title="Tema E", capacity=10, category="Category B"),
        ]

        tutor1 = Tutor(
            1, 1, "Email", "Name", "Lastname", capacity=2, topics=[topics[0], topics[1]]
        )
        tutor2 = Tutor(
            2, 1, "Email", "Name", "Lastname", capacity=2, topics=[topics[2], topics[3]]
        )

        tutors = [tutor1, tutor2]
        solver = GroupTutorFlowSolver(tutors=tutors, topics=topics)
        edges = solver._create_topics_tutors_edges()
        assert len(edges) == 4

    @pytest.mark.unit
    def test_create_tutor_sink_edges(self):
        tutor1 = Tutor(
            1, 1, "Email", "Name", "Lastname", capacity=2, topics=[]
        )
        tutor2 = Tutor(
            2, 1, "Email", "Name", "Lastname", capacity=5, topics=[]
        )

        tutors = [tutor1, tutor2]
        solver = GroupTutorFlowSolver(tutors=tutors)
        edges = solver._create_tutors_sink_edges()
        assert len(edges) == 2

    @pytest.mark.unit
    def test_success(self):
        topics = [
            Topic(id=0, title="Tema C", capacity=10, category="Category A"),
            Topic(id=1, title="Tema A", capacity=10, category="Category A"),
            Topic(id=2, title="Tema B", capacity=10, category="Category A"),
            Topic(id=3, title="Tema E", capacity=10, category="Category B"),
        ]

        groups = [
            UnassignedGroup(
                1,
                topics=[topics[0], topics[1], topics[2]],
                students=["Student 1", "Student 2", "Student 3", "Student 4"],
            ),
            UnassignedGroup(
                2,
                topics=[topics[1], topics[2], topics[3]],
                students=["Student 5", "Student 6", "Student 7", "Student 8"],
            ),
        ]

        tutor1 = Tutor(
            1, 1, "Email", "Name", "Lastname", capacity=2, topics=[topics[0], topics[1]]
        )
        tutor2 = Tutor(
            2, 1, "Email", "Name", "Lastname", capacity=2, topics=[topics[2], topics[3]]
        )

        tutors = [tutor1, tutor2]

        solver = GroupTutorFlowSolver(groups, topics, tutors)
        result = solver.solve()
        assert len(result) == 2
