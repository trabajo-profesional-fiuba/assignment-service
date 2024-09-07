import pytest
import time

from src.core.algorithms.topic_tutor.group_tutor_lp_solver import GroupTutorLPSolver
from src.core.group_topic_preferences import GroupTopicPreferences
from src.core.topic import Topic
from src.core.tutor import Tutor


class TestGroupTutorLPSolver:

    # ------------ Logic Tests ------------
    @pytest.mark.unit
    def test_success(self):
        topics = [
            Topic(id=0, title="Tema C", capacity=10, category="Category A"),
            Topic(id=1, title="Tema A", capacity=10, category="Category A"),
            Topic(id=2, title="Tema B", capacity=10, category="Category A"),
            Topic(id=3, title="Tema E", capacity=10, category="Category B"),
        ]

        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2", "Student 3", "Student 4"]
            ),
            
            GroupTopicPreferences(
                2, topics=[topics[1], topics[2], topics[3]], students=["Student 5", "Student 6", "Student 7", "Student 8"]
            ),
        ]

        tutor1 = Tutor(1, "Email", "Name", "Lastname")
        tutor1.add_topic(topics[0])
        tutor1.add_topic(topics[1])
        tutor1.set_capacity(2)

        tutor2 = Tutor(2, "Email", "Name", "Lastname")
        tutor2.add_topic(topics[2])
        tutor2.add_topic(topics[3])
        tutor2.set_capacity(2)

        tutors = [
            tutor1, tutor2
        ]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=5)
        result = solver.solve()

        assert len(result) == 2

        assert result[0].id == 1
        assert result[0].assigned_topic == topics[0]

        assert result[1].id == 2
        assert result[1].assigned_topic == topics[1]
    
    @pytest.mark.unit
    def test_more_groups_than_tutors_without_enough_capacity(self):
        """Testing that tutors dont get all groups so they dont to
        exceed their capacities."""
        topics = [
            Topic(id=0, title="Topic 1", capacity=3, category="Category A"),
            Topic(id=1, title="Topic 2", capacity=3, category="Category A"),
            Topic(id=2, title="Topic 3", capacity=3, category="Category B"),
            Topic(id=3, title="Topic 4", capacity=3, category="Category B"),
            Topic(id=4, title="Topic 5", capacity=3, category="Category C"),
            Topic(id=5, title="Topic 6", capacity=3, category="Category C"),
        ]

        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2"]
            ),
            GroupTopicPreferences(
                2, topics=[topics[3], topics[4], topics[5]], students=["Student 3", "Student 4"]
            ),
            GroupTopicPreferences(
                3, topics=[topics[0], topics[4], topics[2]], students=["Student 5", "Student 6"]
            ),
        ]

        tutor1 = Tutor(1, "tutor1@example.com", "Tutor 1 name",  "Tutor 1 lastname")
        tutor1.add_topic(topics[0])
        tutor1.add_topic(topics[1])
        tutor1.set_capacity(1)

        tutor2 = Tutor(2, "tutor2@example.com", "Tutor 2 name", "Tutor 2 lastname")
        tutor2.add_topic(topics[2])
        tutor2.add_topic(topics[3])
        tutor2.add_topic(topics[4])
        tutor2.add_topic(topics[5])
        tutor2.set_capacity(1)

        tutors = [tutor1, tutor2]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=5)
        result = solver.solve()
        
        assert len(result) == 3

        assert result[0].id == 1
        assert result[0].assigned_topic == topics[0]

        assert result[1].id == 2
        assert result[1].assigned_topic == topics[3]

        assert result[2].id == 3
        assert result[2].assigned_topic == topics[4]
        
    @pytest.mark.unit
    def test_tutor_group_assignment_balance(self):
        """
        Testing that the difference in the number of groups assigned to each tutor 
        does not exceed the allowed balance limit of 1.
        """
        topics = [
            Topic(id=0, title="Topic 1", capacity=1, category="Category A"),
            Topic(id=1, title="Topic 2", capacity=1, category="Category A"),
            Topic(id=2, title="Topic 3", capacity=1, category="Category B"),
            Topic(id=3, title="Topic 4", capacity=1, category="Category B"),
            Topic(id=4, title="Topic 5", capacity=1, category="Category C"),
            Topic(id=5, title="Topic 6", capacity=1, category="Category C"),
        ]

        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2"]
            ),
            GroupTopicPreferences(
                2, topics=[topics[3], topics[4], topics[5]], students=["Student 3", "Student 4"]
            ),
            GroupTopicPreferences(
                3, topics=[topics[4], topics[0], topics[2]], students=["Student 5", "Student 6"]
            ),
            GroupTopicPreferences(
                4, topics=[topics[2], topics[1], topics[3]], students=["Student 7", "Student 8"]
            ),
        ]

        tutor1 = Tutor(1, "tutor1@example.com", "Tutor 1 name",  "Tutor 1 lastname")
        tutor1.add_topic(topics[0])
        tutor1.add_topic(topics[1])
        tutor1.set_capacity(3)

        tutor2 = Tutor(2, "tutor2@example.com", "Tutor 2 name", "Tutor 2 lastname")
        tutor2.add_topic(topics[2])
        tutor2.add_topic(topics[3])
        tutor2.add_topic(topics[4])
        tutor2.add_topic(topics[5])
        tutor2.set_capacity(3)

        tutors = [tutor1, tutor2]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=1)
        result = solver.solve()

        # Verificar que la diferencia en el número de grupos asignados a los tutores no sea mayor a 1
        tutor1_groups = len([assignment for assignment in result if assignment.tutor.id == tutor1.id])
        tutor2_groups = len([assignment for assignment in result if assignment.tutor.id == tutor2.id])

        assert abs(tutor1_groups - tutor2_groups) <= 1

        # Verificar que todos los grupos hayan sido asignados
        assert len(result) == len(groups)

        assert result[0].id == 1
        assert result[0].assigned_topic == topics[0]

        assert result[1].id == 2
        assert result[1].assigned_topic == topics[3]

        assert result[2].id == 3
        assert result[2].assigned_topic == topics[4]

        assert result[3].id == 4
        assert result[3].assigned_topic == topics[1]

    @pytest.mark.unit
    def test_tutor_without_capacity(self):
        """
        Verifica que el solver no asigne más grupos a un tutor que ha alcanzado su capacidad.
        """
        topics = [
            Topic(id=0, title="Tema 1", capacity=3, category="Category A"),
            Topic(id=1, title="Tema 2", capacity=3, category="Category A"),
            Topic(id=2, title="Tema 3", capacity=3, category="Category A")
        ]

        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2"]),
            GroupTopicPreferences(2, topics=[topics[1], topics[0], topics[2]], students=["Student 3", "Student 4"]),
            GroupTopicPreferences(3, topics=[topics[0], topics[2], topics[1]], students=["Student 5", "Student 6"])
        ]

        tutor1 = Tutor(1, "Email", "Name", "Lastname")
        tutor1.add_topic(topics[0])
        tutor1.add_topic(topics[1])
        tutor1.add_topic(topics[2])
        tutor1.set_capacity(2)

        tutors = [tutor1]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=1)
        result = solver.solve()

        # Verificar que no se asignen más grupos de los permitidos
        assert len(result) == 2
        assigned_groups = [res.id for res in result]
        assert 3 not in assigned_groups  # El grupo 3 no debe ser asignado

    @pytest.mark.unit
    def test_strict_balance_limit(self):
        """
        Verifica que el solver respete estrictamente el balance límite al asignar grupos a los tutores.
        """
        topics = [
            Topic(id=0, title="Topic 1", capacity=2, category="Category A"),
            Topic(id=1, title="Topic 2", capacity=2, category="Category A"),
            Topic(id=2, title="Topic 3", capacity=2, category="Category A")

        ]

        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2"]),
            GroupTopicPreferences(2, topics=[topics[0], topics[1], topics[2]], students=["Student 3", "Student 4"]),
            GroupTopicPreferences(3, topics=[topics[0], topics[2], topics[1]], students=["Student 5", "Student 6"]),
            GroupTopicPreferences(4, topics=[topics[0], topics[1], topics[2]], students=["Student 7", "Student 8"])
        ]

        tutor1 = Tutor(1, "Email", "Name", "Lastname")
        tutor1.add_topic(topics[0])
        tutor1.set_capacity(2)

        tutor2 = Tutor(2, "Email", "Name", "Lastname")
        tutor2.add_topic(topics[1])
        tutor2.set_capacity(2)

        tutors = [tutor1, tutor2]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=1)
        result = solver.solve()

        # Verificar que la diferencia entre grupos asignados a tutor1 y tutor2 sea <= 1
        tutor1_groups = len([res for res in result if res.tutor.id == tutor1.id])
        tutor2_groups = len([res for res in result if res.tutor.id == tutor2.id])
        assert abs(tutor1_groups - tutor2_groups) <= 1

    @pytest.mark.unit
    def test_topic_capacity_exceeded(self):
        """
        Verifica que el solver no asigne más grupos a un tema cuando su capacidad se ha alcanzado.
        """
        topics = [
            Topic(id=0, title="Topic 1", capacity=1, category="Category A"),
            Topic(id=1, title="Topic 2", capacity=2, category="Category B"),
            Topic(id=1, title="Topic 2", capacity=2, category="Category C")
        ]

        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1", "Student 2"]),
            GroupTopicPreferences(2, topics=[topics[0], topics[1], topics[2]], students=["Student 3", "Student 4"]),
            GroupTopicPreferences(3, topics=[topics[1], topics[2], topics[0]], students=["Student 5", "Student 6"])
        ]

        tutor1 = Tutor(1, "Email", "Name", "Lastname")
        tutor1.add_topic(topics[0])
        tutor1.add_topic(topics[1])
        tutor1.set_capacity(3)

        tutors = [tutor1]

        solver = GroupTutorLPSolver(groups, topics, tutors, balance_limit=1)
        result = solver.solve()

        # Verificar que solo un grupo haya sido asignado al Topic 1 (capacidad = 1)
        topic1_assignments = len([res for res in result if res.assigned_topic.id == topics[0].id])
        assert topic1_assignments == 1

        # Verificar que los otros grupos se asignen al Topic 2
        topic2_assignments = len([res for res in result if res.assigned_topic.id == topics[1].id])
        assert topic2_assignments == 2
