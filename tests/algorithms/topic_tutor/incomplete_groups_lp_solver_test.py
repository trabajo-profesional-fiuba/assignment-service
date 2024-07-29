import pytest
from pulp import LpStatus
from src.algorithms.topic_tutor.incomplete_groups_lp_solver import IncompleteGroupsLPSolver
from src.model.group_topic_preferences import GroupTopicPreferences
from src.model.utils.topic import Topic
import csv

# Función para leer el CSV y crear los objetos
def read_csv_and_create_objects(file_path):
    topics = {}
    groups = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        group_id = 2
        
        for row in reader:
            # Crear o obtener los tópicos de las preferencias
            preferences = [row['Preferencia 1'], row['Preferencia 2'], row['Preferencia 3']]
            group_topics = []
            
            if (preferences[0] != 'Ya tenemos tema y tutor, pero vamos a hacer el Trabajo Profesional en el marco de la asignatura') or preferences[1] != 'Ya tenemos tema y tutor, pero vamos a hacer el Trabajo Profesional en el marco de la asignatura':
                for pref in preferences:
                    if pref not in topics:
                        topics[pref] = Topic(len(topics) + 1, pref, 0)
                    group_topics.append(topics[pref])
                
                # Crear los estudiantes, verificando que el correo no esté en blanco
                students = []
                for i in range(1, 5):  # Asumiendo que puede haber hasta 4 correos
                    student_email_key = f'Mail (preferentemente @fi.uba.ar){i}'
                    if row.get(student_email_key):
                        email = row[student_email_key].strip()
                        if email:  # Asegúrate de que el correo no esté vacío
                            students.append(email)
                
                # Crear el grupo y añadirlo a la lista
                group = GroupTopicPreferences(group_id, topics=group_topics, students=students)
                groups.append(group)
                
            group_id += 1
    return topics, groups

class TestIncompleteGroupsLPSolver:

    @pytest.mark.unit
    def test_groups(self):
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0),
            Topic(4, "Tema E", 0),
            Topic(5, "Tema D", 0)
        ]
        
        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"]),
            GroupTopicPreferences(2, topics=[topics[2], topics[3], topics[1]], students=["Student 2", "Student 3"]),
            GroupTopicPreferences(3, topics=[topics[0], topics[4], topics[1]], students=["Student 4", "Student 5"]),
            GroupTopicPreferences(4, topics=[topics[1], topics[4], topics[2]], students=["Student 6", "Student 7"]),
            GroupTopicPreferences(5, topics=[topics[2], topics[3], topics[1]], students=["Student 8", "Student 9"]),
            GroupTopicPreferences(6, topics=[topics[3], topics[3], topics[1]], students=["Student 10"]),
            GroupTopicPreferences(7, topics=[topics[2], topics[0], topics[4]], students=["Student 11"]),
            GroupTopicPreferences(8, topics=[topics[2], topics[0], topics[4]], students=["Student 12"]),
            GroupTopicPreferences(9, topics=[topics[2], topics[0], topics[4]], students=["Student 13"]),
            GroupTopicPreferences(10, topics=[topics[2], topics[0], topics[4]], students=["Student 14"])
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
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0)
        ]
        groups = [GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"])]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()
    
        # Verificar que no hay grupos formados
        assert len(formed_groups) == 1
    
        # Verificar que no hay grupos filtrados
        assert len(filtered_groups) == 0
    
    @pytest.mark.unit
    def test_two_groups_with_different_topics_and_categories(self):
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0),
            Topic(4, "Tema D", 0),
            Topic(5, "Tema E", 0),
            Topic(6, "Tema F", 0)
        ]
        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"]),
            GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3", "Student 4"])
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
            Topic(1, "Tema C", 0, category="Category 1"),
            Topic(2, "Tema A", 0, category="Category 2"),
            Topic(3, "Tema B", 0, category="Category 3"),
            Topic(4, "Tema D", 0, category="Category 3"),
            Topic(5, "Tema E", 0, category="Category 2"),
            Topic(6, "Tema F", 0, category="Category 1")
        ]
        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"]),
            GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3", "Student 4"])
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
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0),
            Topic(4, "Tema D", 0),
            Topic(5, "Tema E", 0),
            Topic(6, "Tema F", 0)
        ]
        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"]),
            GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3"])
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
            Topic(1, "Tema A", 0),
            Topic(2, "Tema B", 0),
            Topic(3, "Tema C", 0),
            Topic(4, "Tema D", 0),
            Topic(5, "Tema E", 0),
            Topic(6, "Tema F", 0)
        ]
        groups = [
            GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"]),
            GroupTopicPreferences(2, topics=[topics[0], topics[3], topics[4]], students=["Student 2", "Student 3"]),
            GroupTopicPreferences(3, topics=[topics[1], topics[3], topics[5]], students=["Student 4", "Student 5"]),
            GroupTopicPreferences(4, topics=[topics[2], topics[4], topics[5]], students=["Student 6", "Student 7"])
        ]

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        # Verificar que se formaron varios grupos
        assert len(formed_groups) == 2

    @pytest.mark.skip
    def test_real_case_1C2024(self):

        # Usar la función para leer el archivo CSV y crear los objetos
        topics, groups = read_csv_and_create_objects('db/test_1c2024.csv')

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        assert len(formed_groups) > 0

    @pytest.mark.skip
    def test_real_case_2C2023(self):

        # Usar la función para leer el archivo CSV y crear los objetos
        topics, groups = read_csv_and_create_objects('db/test_2c2023.csv')

        solver = IncompleteGroupsLPSolver(groups)
        formed_groups, filtered_groups = solver.solve()

        assert len(formed_groups) > 0
