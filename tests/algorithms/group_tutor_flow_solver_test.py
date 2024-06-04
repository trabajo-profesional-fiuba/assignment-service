# import pytest
# import time
# from src.algorithms.group_tutor_flow_solver import (
#     GroupTutorFlowSolver,
# )
# from tests.algorithms.helper import TestHelper
# from src.model.formatter.output.output_formatter import OutputFormatter


# class TestGroupTopicTutorFlowSolver:

#     helper = TestHelper()
#     formatter = OutputFormatter()

#     # ------------ Logic Tests ------------
#     @pytest.mark.unit
#     def test_more_groups_than_tutors_without_enough_capacity(self):
#         """Testing that tutors do not get all groups in order not to exceed their
#         capacities."""
#         group_topics_costs = [
#             [1, 2, 3, 4, 4, 4],  # groups as rows
#             [4, 4, 4, 1, 2, 3],  # topics as columns
#             [1, 4, 2, 4, 3, 4],
#         ]
#         group_topics_capacities = [0, 0, 0, 0, 0, 0]
#         topics_tutors_capacities = [
#             [3, 3, 0, 0, 0, 0],  # tutors as rows
#             [0, 0, 3, 3, 3, 3],  # topics as columns
#         ]
#         topics_tutors_costs = [
#             [1, 1, 0, 0, 0, 0],  # tutors as rows
#             [0, 0, 1, 1, 1, 1],  # topics as columns
#         ]
#         tutors_groups_capacities = [1, 1]

#         groups = self.helper.create_groups(
#             3, 6, group_topics_costs, group_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2,
#             tutors_groups_capacities,
#             6,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         tutors_groups = self.helper.get_tutors_groups(formatted_result)

#         assert len(tutors_groups["tutor-1"]) <= 1
#         assert len(tutors_groups["tutor-2"]) <= 1

#     @pytest.mark.unit
#     def test_more_groups_than_tutors_but_with_enough_capacity(self):
#         """Testing that tutors get all groups without exceeding their capacities."""
#         group_topics_costs = [
#             [1, 2, 3, 4, 4, 4],  # groups as rows
#             [4, 4, 4, 1, 2, 3],  # topics as columns
#             [1, 4, 2, 4, 3, 4],
#         ]
#         group_topics_capacities = [0, 0, 0, 0, 0, 0]
#         tutors_capacities = [1, 2]
#         topics_tutors_capacities = [[3, 3, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3]]
#         topics_tutors_costs = [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1]]

#         groups = self.helper.create_groups(
#             3, 6, group_topics_costs, group_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 6, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         tutors_groups = self.helper.get_tutors_groups(formatted_result)
#         assert len(tutors_groups["tutor-1"]) <= 1
#         assert len(tutors_groups["tutor-2"]) <= 2

#     @pytest.mark.unit
#     def test_equal_groups_and_tutors_but_tutors_do_not_exceed_their_capacities(self):
#         """Testing that tutors get all groups without exceeding their capacities."""
#         group_topics_costs = [
#             [1, 2, 3, 4, 4, 4],
#             [4, 4, 4, 1, 2, 3],
#             [1, 4, 2, 4, 3, 4],
#         ]
#         group_topics_capacities = [0, 0, 0, 0, 0, 0]
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

#         groups = self.helper.create_groups(
#             3, 6, group_topics_costs, group_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             3, tutors_capacities, 6, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         tutors_groups = self.helper.get_tutors_groups(formatted_result)
#         assert len(tutors_groups["tutor-1"]) <= 1
#         assert len(tutors_groups["tutor-2"]) <= 1
#         assert len(tutors_groups["tutor-3"]) <= 1

#     @pytest.mark.unit
#     def test_more_tutors_than_groups_but_tutors_do_not_exceed_their_capacities(self):
#         """Testing that groups are distributed between tutors in order not to
#         exceed their capacities."""
#         groups_topics_costs = [
#             [1, 2, 3, 4, 4, 4],
#             [4, 4, 4, 1, 2, 3],
#         ]
#         group_topics_capacities = [0, 0, 0, 0, 0, 0]
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

#         groups = self.helper.create_groups(
#             2, 6, groups_topics_costs, group_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             3, tutors_capacities, 6, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         tutors_groups = self.helper.get_tutors_groups(formatted_result)
#         for tutor, groups in tutors_groups.items():
#             assert len(groups) <= 1

#     @pytest.mark.unit
#     def test_equal_groups_and_topics_so_every_group_is_assigned_to_one_topic(self):
#         """Testing all groups are assigned to one topic when there are enough
#         tutors with enough capacities."""
#         groups_topics_costs = [
#             [1, 2],
#             [4, 4],
#         ]
#         groups_topics_capacities = [0, 0]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [
#             [1, 0],
#             [0, 1],
#         ]
#         topics_tutors_costs = [
#             [1, 1],
#             [1, 1],
#         ]

#         groups = self.helper.create_groups(
#             2, 2, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 2, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 2

#     @pytest.mark.unit
#     def test_more_groups_than_topics_but_tutors_with_enough_capacity(self):
#         """Testing all groups are assigned to one topic when there are more groups
#         than topics but tutors with enough capacities."""
#         groups_topics_costs = [
#             [1],
#             [4],
#         ]
#         groups_topics_capacities = [0]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [[1], [1]]
#         topics_tutors_costs = [[1], [1]]

#         groups = self.helper.create_groups(
#             2, 1, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 1, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 2

#     @pytest.mark.unit
#     def test_more_groups_but_tutor_with_enough_capacity(self):
#         """Testing all groups are assigned to one topic when there are more groups
#         than topics and tutors but tutor with enough capacity."""
#         groups_topics_costs = [
#             [1],
#             [4],
#         ]
#         groups_topics_capacities = [0]
#         tutors_capacities = [2]
#         topics_tutors_capacities = [
#             [2],
#         ]
#         topics_tutors_costs = [
#             [1],
#         ]

#         groups = self.helper.create_groups(
#             2, 1, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             1, tutors_capacities, 1, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) == 2

#     @pytest.mark.unit
#     def test_more_topics_than_groups_and_one_topic_is_assigned_to_each_group(self):
#         """Testing only one topic is assigned to every group when there are more
#         groups than topics."""
#         groups_topics_costs = [
#             [1, 2, 1, 2],
#             [1, 2, 1, 2],
#         ]
#         groups_topics_capacities = [0, 0, 0, 0]
#         tutors_capacities = [2, 2]
#         topics_tutors_capacities = [
#             [1, 0, 1, 0],
#             [0, 1, 1, 0],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 1, 1],
#             [1, 1, 1, 1],
#         ]

#         groups = self.helper.create_groups(
#             2, 4, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 4, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)

#         all_topics = ["topic-1", "topic-2", "topic-3", "topic-4"]
#         all_topics.remove(groups_topics["group-1"][0])
#         all_topics.remove(groups_topics["group-2"][0])
#         not_assigned_topics = all_topics
#         assert len(not_assigned_topics) > 0

#     @pytest.mark.unit
#     def test_groups_with_same_preferences_and_tutors_with_capacity(self):
#         """Testing groups with same preferences and costs are assigned to the same
#         topic since it is assigned to tutors that has enough capacity."""
#         groups_topics_costs = [
#             [1, 2],
#             [1, 2],
#         ]
#         groups_topics_capacities = [0, 0]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [
#             [1, 1],
#             [1, 1],
#         ]
#         topics_tutors_costs = [
#             [1, 1],
#             [1, 1],
#         ]

#         groups = self.helper.create_groups(
#             2, 2, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 2, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert groups_topics["group-1"][0] == groups_topics["group-2"][0]

#     @pytest.mark.unit
#     def test_groups_with_same_preferences_but_tutor_capacity_not_enough(self):
#         """Testing groups with same preferences and costs are not assigned
#         to the same topic which is assigned to only one tutor and this
#         tutor does not have enough capacity."""
#         groups_topics_costs = [
#             [1, 2],
#             [1, 2],
#         ]
#         groups_topics_capacities = [0, 0]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [
#             [1, 0],
#             [0, 1],
#         ]
#         topics_tutors_costs = [
#             [1, 1],
#             [1, 1],
#         ]

#         groups = self.helper.create_groups(
#             2, 2, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 2, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert groups_topics["group-1"][0] != groups_topics["group-2"][0]

#     # ------------ Quality Tests ------------
#     @pytest.mark.unit
#     def test_two_groups_with_different_preferences(self):
#         """Testing two groups with different preferences and can not be assigned
#         a topic with low preference."""
#         groups_topics_costs = [
#             [1, 2, 3],  # group-1 preferences: topic-1, topic-2, topic-3
#             [2, 1, 3],  # group-2 preferences: topic-2, topic-1, topic-3
#         ]
#         groups_topics_capacities = [0, 0, 0]
#         tutors_capacities = [1, 1]
#         topics_tutors_capacities = [
#             [1, 1, 1],
#             [1, 1, 1],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 1],
#             [1, 1, 1],
#         ]

#         groups = self.helper.create_groups(
#             2, 3, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 3, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)

#         assert groups_topics["group-1"][0] == "topic-1"
#         assert groups_topics["group-2"][0] == "topic-2"

#     @pytest.mark.unit
#     def test_more_groups_with_different_preferences(self):
#         """Testing a group can not be assigned a topic with low preference if
#         the topic that it was chosen is available."""
#         groups_topics_costs = [
#             [1, 2, 3],  # group-1 preferences: topic-1, topic-2, topic-3
#             [2, 1, 3],  # group-2 preferences: topic-2, topic-1, topic-3
#             [3, 2, 1],  # group-3 preferences: topic-3, topic-2, topic-1
#         ]
#         groups_topics_capacities = [0, 0, 0]
#         tutors_capacities = [2, 1]
#         topics_tutors_capacities = [
#             [1, 1, 1],
#             [1, 1, 1],
#         ]
#         topics_tutors_costs = [
#             [1, 1, 1],
#             [1, 1, 1],
#         ]

#         groups = self.helper.create_groups(
#             3, 3, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             2, tutors_capacities, 3, topics_tutors_capacities, topics_tutors_costs
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         result = solver.solve()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)

#         assert groups_topics["group-1"][0] == "topic-1"
#         assert groups_topics["group-2"][0] == "topic-2"
#         assert groups_topics["group-3"][0] == "topic-3"

#     # ------------ Performance and Scalability Tests ------------
#     @pytest.mark.performance
#     def test_four_groups_and_topics(self):
#         """Testing if the algorithm is overhead with four groups and topics."""
#         num_groups = 4
#         num_topics = 4
#         num_tutors = 2

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "4 groups, 4 topics, 2 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_ten_groups_and_topics(self):
#         """Testing if the algorithm is overhead with ten groups and topics."""
#         num_groups = 10
#         num_topics = 10
#         num_tutors = 5

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "10 groups, 10 topics, 5 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_twenty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with twenty groups and topics."""
#         num_groups = 20
#         num_topics = 20
#         num_tutors = 10

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "20 groups, 20 topics, 10 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_forty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with forty groups and topics."""
#         num_groups = 40
#         num_topics = 40
#         num_tutors = 20

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "40 groups, 40 topics, 20 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_eighty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with eighty groups and topics."""
#         num_groups = 80
#         num_topics = 80
#         num_tutors = 40

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)
#         assert len(groups_topics.items()) > 0
#         print(
#             "80 groups, 80 topics, 40 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_one_hundred_and_sixty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with one hundred and sixty groups
#         and topics."""
#         num_groups = 160
#         num_topics = 160
#         num_tutors = 80

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)

#         assert len(groups_topics.items()) > 0
#         print(
#             "160 groups, 160 topics, 80 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )

#     @pytest.mark.performance
#     def test_three_hundred_and_twenty_groups_and_topics(self):
#         """Testing if the algorithm is overhead with three hundred and twenty groups
#         and topics."""
#         num_groups = 320
#         num_topics = 320
#         num_tutors = 160

#         groups_topics_costs = self.helper.create_matrix(num_groups, num_topics, True, 4)
#         groups_topics_capacities = self.helper.create_list(num_topics, 0)
#         tutors_capacities = self.helper.create_list(num_groups, 2)
#         topics_tutors_capacities = self.helper.create_matrix(
#             num_tutors, num_topics, False, 2
#         )
#         topics_tutors_costs = self.helper.create_matrix(
#             num_tutors, num_topics, False, 1
#         )

#         groups = self.helper.create_groups(
#             num_groups, num_topics, groups_topics_costs, groups_topics_capacities
#         )
#         tutors = self.helper.create_tutors(
#             num_tutors,
#             tutors_capacities,
#             num_topics,
#             topics_tutors_capacities,
#             topics_tutors_costs,
#         )

#         solver = GroupTutorFlowSolver(groups, tutors)
#         start_time = time.time()
#         result = solver.solve()
#         end_time = time.time()

#         formatted_result = self.formatter.format_result(result)
#         groups_topics = self.helper.get_groups_topics(formatted_result)

#         assert len(groups_topics.items()) > 0
#         print(
#             "320 groups, 320 topics, 160 tutors - Execution time:",
#             end_time - start_time,
#             "seconds",
#         )
