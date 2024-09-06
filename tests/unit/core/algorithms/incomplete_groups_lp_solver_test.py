import pytest
from src.core.algorithms.topic_tutor.incomplete_groups_lp_solver import (
    IncompleteGroupsLPSolver,
)
from src.core.group_topic_preferences import GroupTopicPreferences
from src.core.topic import Topic
import csv


# Función para leer el CSV y crear los objetos
def read_csv_and_create_objects(file_path):
    topics = {}
    groups = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        group_id = 2

        for row in reader:
            # Crear o obtener los tópicos de las preferencias
            preferences = [
                row["Preferencia_1"],
                row["Preferencia_2"],
                row["Preferencia_3"],
            ]
            group_topics = []

            if (
                (
                    preferences[0]
                    != "Ya tenemos tema y tutor, pero vamos a hacer el Trabajo \
                        Profesional en el marco de la asignatura"
                )
                or preferences[1]
                != "Ya tenemos tema y tutor, pero vamos a hacer el Trabajo Profesional\
                en el marco de la asignatura"
            ):
                for pref in preferences:
                    if pref not in topics:
                        topics[pref] = Topic(len(topics) + 1, pref, 0)
                    group_topics.append(topics[pref])

                # Crear los estudiantes, verificando que el correo no esté en blanco
                students = []
                for i in range(1, 5):  # Asumiendo que puede haber hasta 4 correos
                    student_email_key = f"Mail (preferentemente @fi.uba.ar){i}"
                    if row.get(student_email_key):
                        email = row[student_email_key].strip()
                        if email:  # Asegúrate de que el correo no esté vacío
                            students.append(email)

                # Crear el grupo y añadirlo a la lista
                group = GroupTopicPreferences(
                    group_id, topics=group_topics, students=students
                )
                groups.append(group)

            group_id += 1
    return topics, groups


class TestIncompleteGroupsLPSolver:

    @pytest.mark.unit
    def test_groups(self):
        topics = [
            Topic(id=1, title="Tema_C", capacity=0, category="Category A"),
            Topic(id=2, title="Tema_A", capacity=0, category="Category A"),
            Topic(id=3, title="Tema_B", capacity=0, category="Category A"),
            Topic(id=4, title="Tema_E", capacity=0, category="Category A"),
            Topic(id=5, title="Tema_D", capacity=0, category="Category A"),
        ]

        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            ),
            GroupTopicPreferences(
                2,
                topics=[topics[2], topics[3], topics[1]],
                students=["Student_2", "Student_3"],
            ),
            GroupTopicPreferences(
                3,
                topics=[topics[0], topics[4], topics[1]],
                students=["Student_4", "Student_5"],
            ),
            GroupTopicPreferences(
                4,
                topics=[topics[1], topics[4], topics[2]],
                students=["Student_6", "Student_7"],
            ),
            GroupTopicPreferences(
                5,
                topics=[topics[2], topics[3], topics[1]],
                students=["Student_8", "Student_9"],
            ),
            GroupTopicPreferences(
                6, topics=[topics[3], topics[3], topics[1]], students=["Student_10"]
            ),
            GroupTopicPreferences(
                7, topics=[topics[2], topics[0], topics[4]], students=["Student_11"]
            ),
            GroupTopicPreferences(
                8, topics=[topics[2], topics[0], topics[4]], students=["Student_12"]
            ),
            GroupTopicPreferences(
                9, topics=[topics[2], topics[0], topics[4]], students=["Student_13"]
            ),
            GroupTopicPreferences(
                10, topics=[topics[2], topics[0], topics[4]], students=["Student_14"]
            ),
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que se formaron los grupos correctos
        assert len(formed_groups) == 4

    @pytest.mark.unit
    def test_no_groups(self):
        groups = []
        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que no hay grupos formados
        assert len(formed_groups) == 0

        # Verificar que no hay grupos filtrados
        assert len(filtered_groups) == 0

    @pytest.mark.unit
    def test_single_group(self):
        topics = [Topic(id=1, title="Tema_C", capacity=0, category="Category A"), Topic(id=2, title="Tema_A", capacity=0, category="Category A"), Topic(id=3, title="Tema_B", capacity=0, category="Category A")]
        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            )
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que no hay grupos formados
        assert len(formed_groups) == 1

        # Verificar que no hay grupos filtrados
        assert len(filtered_groups) == 0

    @pytest.mark.unit
    def test_two_groups_with_different_topics_and_categories(self):
        topics = [
            Topic(id=1, title="Tema_C", capacity=0, category="Category A"),
            Topic(id=2, title="Tema_A", capacity=0, category="Category A"),
            Topic(id=3, title="Tema_B", capacity=0, category="Category A"),
            Topic(id=4, title="Tema_D", capacity=0, category="Category A"),
            Topic(id=5, title="Tema_E", capacity=0, category="Category A"),
            Topic(id=6, title="Tema_F", capacity=0, category="Category A"),
        ]
        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            ),
            GroupTopicPreferences(
                2,
                topics=[topics[3], topics[4], topics[5]],
                students=["Student_2", "Student_3", "Student_4"],
            ),
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que se formó un grupo con los estudiantes de ambos grupos
        assert len(formed_groups) == 1

        # Verificar que no hay grupos restantes
        assert len(filtered_groups) == 0

    @pytest.mark.unit
    def test_two_groups_with_same_category(self):
        topics = [
            Topic(id=1, title="Tema_C", capacity=0, category="Category_1"),
            Topic(id=2, title="Tema_A", capacity=0, category="Category_2"),
            Topic(id=3, title="Tema_B", capacity=0, category="Category_3"),
            Topic(id=4, title="Tema_D", capacity=0, category="Category_3"),
            Topic(id=5, title="Tema_E", capacity=0, category="Category_2"),
            Topic(id=6, title="Tema_F", capacity=0, category="Category_1"),
        ]
        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            ),
            GroupTopicPreferences(
                2,
                topics=[topics[3], topics[4], topics[5]],
                students=["Student_2", "Student_3", "Student_4"],
            ),
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que se formó un grupo con los estudiantes de ambos grupos
        assert len(formed_groups) == 1

        # Verificar que no hay grupos restantes
        assert len(filtered_groups) == 0

    @pytest.mark.unit
    def test_two_groups_with_different_topics_with_three_students(self):
        topics = [
            Topic(id=1, title="Tema_C", capacity=0, category="Category A"),
            Topic(id=2, title="Tema_A", capacity=0, category="Category A"),
            Topic(id=3, title="Tema_B", capacity=0, category="Category A"),
            Topic(id=4, title="Tema_D", capacity=0, category="Category A"),
            Topic(id=5, title="Tema_E", capacity=0, category="Category A"),
            Topic(id=6, title="Tema_F", capacity=0, category="Category A"),
        ]
        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            ),
            GroupTopicPreferences(
                2,
                topics=[topics[3], topics[4], topics[5]],
                students=["Student_2", "Student_3"],
            ),
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que se formó un grupo con los estudiantes de ambos grupos
        assert len(formed_groups) == 1

        # Verificar que no hay grupos restantes
        assert len(filtered_groups) == 0

    @pytest.mark.unit
    def test_multiple_groups(self):
        topics = [
            Topic(id=1, title="Tema_A", capacity=0, category="Category A"),
            Topic(id=2, title="Tema_B", capacity=0, category="Category A"),
            Topic(id=3, title="Tema_C", capacity=0, category="Category A"),
            Topic(id=4, title="Tema_D", capacity=0, category="Category A"),
            Topic(id=5, title="Tema_E", capacity=0, category="Category A"),
            Topic(id=6, title="Tema_F", capacity=0, category="Category A"),
        ]
        groups = [
            GroupTopicPreferences(
                1, topics=[topics[0], topics[1], topics[2]], students=["Student_1"]
            ),
            GroupTopicPreferences(
                2,
                topics=[topics[0], topics[3], topics[4]],
                students=["Student_2", "Student_3"],
            ),
            GroupTopicPreferences(
                3,
                topics=[topics[1], topics[3], topics[5]],
                students=["Student_4", "Student_5"],
            ),
            GroupTopicPreferences(
                4,
                topics=[topics[2], topics[4], topics[5]],
                students=["Student_6", "Student_7"],
            ),
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, _ = solver.solve()

        # Verificar que se formaron varios grupos
        assert len(formed_groups) == 2

    @pytest.mark.skip
    def test_real_case_1C2024(self):

        # Usar la función para leer el archivo CSV y crear los objetos
        topics, groups = read_csv_and_create_objects("db/test_1c2024.csv")

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        assert len(formed_groups) > 0

    @pytest.mark.skip
    def test_real_case_2C2023(self):

        # Usar la función para leer el archivo CSV y crear los objetos
        topics, groups = read_csv_and_create_objects("db/test_2c2023.csv")

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        assert len(formed_groups) > 0
