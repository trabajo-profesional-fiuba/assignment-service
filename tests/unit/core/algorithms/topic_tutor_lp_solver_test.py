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


    # @pytest.mark.unit
    # def test_more_groups_than_tutors_but_with_enough_capacity_all_groups_are_assigned(
    #     self,
    # ):
    #     """Testing that tutors get all groups without exceeding their capacities."""
    #     group_costs = [[1, 2, 3, 4, 4, 4], [4, 4, 4, 1, 2, 3], [1, 4, 2, 4, 3, 4]]
    #     tutors_capacities = [1, 2]
    #     topics_tutors_capacities = [[3, 3, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3]]
    #     topics_tutors_costs = [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1]]

    #     groups = self.helper.create_groups(3, group_costs)
    #     topics = self.helper.create_topics(6)
    #     tutors = self.helper.create_tutors(
    #         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
    #     )

    #     solver = GroupTutorLPSolver(groups, topics, tutors)
    #     result = solver.solve_simplex()

    #     formatted_result = self.formatter.format_result(result)
    #     groups_topics = self.helper.get_groups_topics(formatted_result)
    #     assert len(groups_topics.items()) == 3

#     @pytest.mark.unit
#     def test_equal_groups_and_tutors_but_tutors_do_not_exceed_their_capacities(self):
#         """Testing that tutors get all groups without exceeding their capacities."""
#         group_costs = [[1, 2, 3, 4, 4, 4], [4, 4, 4, 1, 2, 3], [1, 4, 2, 4, 3, 4]]
#         tutors_capacities = [1, 1, 1]
#         topics_tutors_capacities = [
#             [3, 3, 0, 0, 0, 0],
#             [0, 0, 3, 3, 3, 3],
#             [0, 0, 3, 3, 3, 3],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 0, 0, 0, 0],
#             [0, 0, 1, 1, 1, 1],
#             [0, 0, 1, 1, 1, 1],
#         ]

#         groups = self.helper.create_groups(3, group_costs)
#         topics = self.helper.create_topics(6)
#         tutors = self.helper.create_tutors(
#             3, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 3

#     @pytest.mark.unit
#     def test_more_tutors_than_groups_but_tutors_do_not_exceed_their_capacities(self):
#         """Testing that groups are distributed between tutors in order not
#         to exceed their capacities."""
#         group_costs = [
#             [1, 2, 3, 4, 4, 4],
#             [4, 4, 4, 1, 2, 3],
#         ]
#         tutors_capacities = [1, 1, 1]
#         topics_tutors_capacities = [
#             [3, 3, 0, 0, 0, 0],
#             [0, 0, 3, 3, 3, 3],
#             [0, 0, 3, 3, 3, 3],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 0, 0, 0, 0],
#             [0, 0, 1, 1, 1, 1],
#             [0, 0, 1, 1, 1, 1],
#         ]

#         groups = self.helper.create_groups(2, group_costs)
#         topics = self.helper.create_topics(6)
#         tutors = self.helper.create_tutors(
#             3, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()
#         formatted_result = self.formatter.format_result(result)
#         tutors_groups = self.helper.get_tutors_groups(formatted_result)
#         for tutor, groups in tutors_groups.items():
#             assert len(groups) <= 1

#     @pytest.mark.unit
#     def test_more_groups_than_topics_but_tutors_with_enough_capacity(self):
#         """Testing all groups are assigned to one topic when there are more groups
#           than topics but tutors with enough capacities."""
#         group_costs = [
#             [1],
#             [4],
#         ]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [[1], [1]]
#         topics_tutors_costs = [[1], [1]]

#         groups = self.helper.create_groups(2, group_costs)
#         topics = self.helper.create_topics(1)
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 2

#     @pytest.mark.unit
#     def test_more_topics_than_groups_and_one_topic_is_assigned_to_each_group(self):
#         """Testing only one topic is assigned to every group when there are more
#         groups than topics."""
#         group_costs = [
#             [1, 2, 1, 2],
#             [1, 2, 1, 2],
#         ]
#         tutors_capacities = [2, 2]
#         topics_tutors_capacities = [
#             [1, 0, 1, 0],
#             [0, 1, 1, 0],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 1, 1],
#             [1, 1, 1, 1],
#         ]

#         groups = self.helper.create_groups(2, group_costs)
#         topics = self.helper.create_topics(4)
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         for group, topics in groups_topics.items():
#             assert len(topics) == 1

#     # ------------ Performance and Scalability Tests ------------
#     @pytest.mark.performance
#     def test_four_groups_and_topics(self):
#         """Testing if the algorithm is overhead with four groups and topics."""
#         num_groups = 4
#         num_topics = 4
#         num_tutors = 2

#         group_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(num_groups, group_costs)
#         topics = self.helper.create_topics(num_topics)
#         tutors = self.helper.create_tutors(
#             num_tutors, tutors_capacities, topics_tutors_capacities,
#               topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         start_time = time.time()
#         result = solver.solve_simplex()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "[simplex solver]: 4 groups, 4 topics, 2 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_ten_groups_and_topics(self):
#         """Testing if the algorithm is overhead with ten groups and topics."""
#         num_groups = 10
#         num_topics = 10
#         num_tutors = 5

#         group_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(num_groups, group_costs)
#         topics = self.helper.create_topics(num_topics)
#         tutors = self.helper.create_tutors(
#             num_tutors, tutors_capacities, topics_tutors_capacities,
# topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         start_time = time.time()
#         result = solver.solve_simplex()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "[simplex solver]: 10 groups, 10 topics, 5 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_twenty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with twenty groups and topics."""
#         num_groups = 20
#         num_topics = 20
#         num_tutors = 10

#         group_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(num_groups, group_costs)
#         topics = self.helper.create_topics(num_topics)
#         tutors = self.helper.create_tutors(
#             num_tutors, tutors_capacities, topics_tutors_capacities,
#               topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         start_time = time.time()
#         result = solver.solve_simplex()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "[simplex solver]: 20 groups, 20 topics, 10 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_test_forty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with forty groups and topics."""
#         num_groups = 40
#         num_topics = 40
#         num_tutors = 20

#         group_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(num_groups, group_costs)
#         topics = self.helper.create_topics(num_topics)
#         tutors = self.helper.create_tutors(
#             num_tutors, tutors_capacities, topics_tutors_capacities,
#              topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         start_time = time.time()
#         result = solver.solve_simplex()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "[simplex solver]: 40 groups, 40 topics, 20 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_eighty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with eighty groups and topics."""
#         num_groups = 80
#         num_topics = 80
#         num_tutors = 40

#         group_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(num_groups, group_costs)
#         topics = self.helper.create_topics(num_topics)
#         tutors = self.helper.create_tutors(
#             num_tutors, tutors_capacities, topics_tutors_capacities,
#               topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         start_time = time.time()
#         result = solver.solve_simplex()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "[simplex solver]: 80 groups, 80 topics, 4 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )
