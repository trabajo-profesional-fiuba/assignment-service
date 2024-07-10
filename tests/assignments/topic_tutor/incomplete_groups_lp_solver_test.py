import pytest
from pulp import LpStatus
from src.assignments.topic_tutor.incomplete_groups_lp_solver import IncompleteGroupsLPSolver
from src.model.group_topic_preferences import GroupTopicPreferences
from src.model.utils.topic import Topic

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
            GroupTopicPreferences(1, [topics[0], topics[1], topics[2]]),
            GroupTopicPreferences(2, [topics[2], topics[3], topics[1]]),
            GroupTopicPreferences(3, [topics[0], topics[4], topics[1]]),
            GroupTopicPreferences(4, [topics[1], topics[4], topics[2]]),
            GroupTopicPreferences(5, [topics[2], topics[3], topics[1]]),
            GroupTopicPreferences(6, [topics[3], topics[3], topics[1]]),
            GroupTopicPreferences(7, [topics[2], topics[0], topics[4]]),
            GroupTopicPreferences(8, [topics[2], topics[0], topics[4]]),
            GroupTopicPreferences(9, [topics[2], topics[0], topics[4]]),
            GroupTopicPreferences(10, [topics[2], topics[0], topics[4]])
        ]

        # Añadir estudiantes a los grupos
        groups[0].add_student("Student 1")
        groups[1].add_student("Student 2")
        groups[1].add_student("Student 3")
        groups[2].add_student("Student 4")
        groups[2].add_student("Student 5")
        groups[3].add_student("Student 6")
        groups[3].add_student("Student 7")
        groups[4].add_student("Student 8")
        groups[4].add_student("Student 9")
        groups[5].add_student("Student 10")
        groups[6].add_student("Student 11")
        groups[7].add_student("Student 12")
        groups[8].add_student("Student 13")
        groups[9].add_student("Student 14")

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()

        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"

        # Verificar que las variables tienen valores esperados
        for var in prob.variables():
            print(f"{var.name}: {var.varValue}")
            if "Unión" in var.name:
                assert var.varValue in [0, 1]

    @pytest.mark.unit
    def test_no_groups(self):
        groups = []
        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 0

    @pytest.mark.unit
    def test_single_group(self):
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0)
        ]
        groups = [GroupTopicPreferences(1, [topics[0], topics[1], topics[2]])]
        groups[0].add_student("Student 1")
    
        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 0
    
    @pytest.mark.unit
    def test_two_groups_with_different_topics(self):
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0),
            Topic(4, "Tema D", 0),
            Topic(5, "Tema E", 0),
            Topic(6, "Tema F", 0)
        ]
        groups = [GroupTopicPreferences(1, [topics[0], topics[1], topics[2]])]
        groups[0].add_student("Student 1")
        groups.append(GroupTopicPreferences(2, [topics[3], topics[4], topics[5]]))
        groups[1].add_student("Student 2")
        groups[1].add_student("Student 3")
        groups[1].add_student("Student 4")

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 1
    
    @pytest.mark.skip
    def test_two_groups_with_different_topics_with_three_students(self):
        topics = [
            Topic(1, "Tema C", 0),
            Topic(2, "Tema A", 0),
            Topic(3, "Tema B", 0),
            Topic(4, "Tema D", 0),
            Topic(5, "Tema E", 0),
            Topic(6, "Tema F", 0)
        ]
        groups = [GroupTopicPreferences(1, [topics[0], topics[1], topics[2]])]
        groups[0].add_student("Student 1")
        groups.append(GroupTopicPreferences(2, [topics[3], topics[4], topics[5]]))
        groups[1].add_student("Student 2")
        groups[1].add_student("Student 3")

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 1

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
            GroupTopicPreferences(1, [topics[0], topics[1], topics[2]]),
            GroupTopicPreferences(2, [topics[0], topics[3], topics[4]]),
            GroupTopicPreferences(3, [topics[1], topics[3], topics[5]]),
            GroupTopicPreferences(4, [topics[2], topics[4], topics[5]])
        ]

        groups[0].add_student("Student 1")
        groups[1].add_student("Student 2")
        groups[1].add_student("Student 3")
        groups[2].add_student("Student 4")
        groups[2].add_student("Student 5")
        groups[3].add_student("Student 6")
        groups[3].add_student("Student 7")

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()

        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"

        # Verificar que las variables tienen valores esperados
        for var in prob.variables():
            print(f"{var.name}: {var.varValue}")
            if "Unión" in var.name:
                assert var.varValue in [0, 1]
