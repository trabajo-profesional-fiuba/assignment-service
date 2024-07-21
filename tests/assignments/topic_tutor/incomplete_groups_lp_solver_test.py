import pytest
from pulp import LpStatus
from src.algorithms.topic_tutor.incomplete_groups_lp_solver import IncompleteGroupsLPSolver
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
        prob = solver.solve()

        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"

        # Verificar que las variables tienen valores esperados
        for var in prob.variables():
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
        groups = [GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]])]
        groups[0].add_student("Student 1")
    
        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 0
    
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
        groups = [GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"])]
        groups.append(GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3", "Student 4"]))

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Union" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 1
    
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
        groups = [GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"])]
        groups.append(GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3", "Student 4"]))

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()

        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"

        # Verificar que los grupos se unen basándose en categorías comunes
        valid_union_vars = [var for var in prob.variables() if "Union" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 1


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
        groups = [GroupTopicPreferences(1, topics=[topics[0], topics[1], topics[2]], students=["Student 1"])]
        groups.append(GroupTopicPreferences(2, topics=[topics[3], topics[4], topics[5]], students=["Student 2", "Student 3"]))

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()
    
        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"
    
        # Verificar que no hay uniones válidas en la solución
        valid_union_vars = [var for var in prob.variables() if "Unión" in var.name and var.varValue == 1]
        assert len(valid_union_vars) == 0

        # Verificar que los grupos restantes se unieron correctamente
        remaining_groups = solver.remaining_groups
        assert len(remaining_groups) == 0

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
            GroupTopicPreferences(3, topics=[topics[1], topics[3], topics[5]], students=["Student 4", "Student 4"]),
            GroupTopicPreferences(4, topics=[topics[2], topics[4], topics[5]], students=["Student 6", "Student 7"])
        ]

        solver = IncompleteGroupsLPSolver(groups)
        prob = solver.solve()

        # Verificar que la solución es óptima
        assert LpStatus[prob.status] == "Optimal"

        # Verificar que las variables tienen valores esperados
        for var in prob.variables():
            print(f"{var.name}: {var.varValue}")
            if "Unión" in var.name:
                assert var.varValue in [0, 1]
