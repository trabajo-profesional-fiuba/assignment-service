# import pytest
# import time

# from src.algorithms.group_tutor_lp_solver import GroupTutorLPSolver
# from tests.algorithms.helper import TestHelper
# from src.io.output.output_formatter import OutputFormatter


# class TestGroupTutorLPSolver:

#     helper = TestHelper()
#     formatter = OutputFormatter()

#     # ------------ Logic Tests ------------
#     @pytest.mark.unit
#     def test_more_groups_than_tutors_without_enough_capacity(self):
#         """Testing that tutors dont get all groups so they dont to
#         exceed their capacities."""
#         group_costs = [
#             [1, 2, 3, 4, 4, 4],  # groups as rows
#             [4, 4, 4, 1, 2, 3],  # topics as columns
#             [1, 4, 2, 4, 3, 4],
#         ]
#         topics_tutors_capacities = [
#             [3, 3, 0, 0, 0, 0],  # tutors as rows
#             [0, 0, 3, 3, 3, 3],  # topics as columns
#         ]
#         topics_tutors_costs = [
#             [1, 1, 0, 0, 0, 0],  # tutors as rows
#             [0, 0, 1, 1, 1, 1],  # topics as columns
#         ]
#         tutors_capacities = [1, 1]

#         groups = self.helper.create_groups(3, group_costs)
#         topics = self.helper.create_topics(6)
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 2

#     @pytest.mark.unit
#     def test_more_groups_than_tutors_but_with_enough_capacity_all_groups_are_assigned(
#         self,
#     ):
#         """Testing that tutors get all groups without exceeding their capacities."""
#         group_costs = [[1, 2, 3, 4, 4, 4], [4, 4, 4, 1, 2, 3], [1, 4, 2, 4, 3, 4]]
#         tutors_capacities = [1, 2]
#         topics_tutors_capacities = [[3, 3, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3]]
#         topics_tutors_costs = [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1]]

#         groups = self.helper.create_groups(3, group_costs)
#         topics = self.helper.create_topics(6)
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorLPSolver(groups, topics, tutors)
#         result = solver.solve_simplex()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 3

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
#         """Testing all groups are assigned to one topic when there are more groups than
#         topics but tutors with enough capacities."""
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
#             num_tutors, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
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
#             num_tutors, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
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
#             num_tutors, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
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
#             num_tutors, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
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
#             num_tutors, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
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
