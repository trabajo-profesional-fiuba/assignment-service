"""Module testing logical of simplex algorithm."""
from src.algorithms.simplex_solver import SimplexSolver
from tests.algorithms.simplex.helper import create_vector, get_all_entities, get_teams_topics, get_topics, get_topics_tutors
import pytest

@pytest.mark.unit
def test_more_teams_than_tutors_without_enough_capacity_so_there_are_teams_without_tutor():
    """Testing that tutors do not get all teams in order not to exceed their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities) # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(team_topic, topic_tutor, topics_c)  # Run the optimization
    
    assert len(teams_topics_tutors.items()) == 2

@pytest.mark.unit
def test_more_teams_than_tutors_but_with_enough_capacity_so_all_teams_are_assigned_to_a_tutor():
    """Testing that tutors get all teams without exceeding their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    tutor_capacities = [1,2]
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities) # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(team_topic, topic_tutor, topics_c)  # Run the optimization

    #Improve assert to be more accurate and avoid edge cases
    assert len(teams_topics_tutors.items()) == 3

@pytest.mark.unit
def test_equal_teams_and_tutors_but_tutors_do_not_exceed_their_capacities():
    """Testing that tutors get all teams without exceeding their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 3
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities) # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(team_topic, topic_tutor, topics_c)  # Run the optimization

    #Improve assert to be more accurate and avoid edge cases
    assert len(teams_topics_tutors.items()) == 3

@pytest.mark.unit
def test_more_tutors_than_groups_but_tutors_do_not_exceed_their_capacities():
    num_groups = 3
    num_topics = 6
    num_tutors = 6
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities) # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(team_topic, topic_tutor, topics_c)  # Run the optimization

    #Improve assert to be more accurate and avoid edge cases
    assert {1: {'t1': 'p2'}, 2: {'t2': 'p1'}, 3: {'t3': 'p4'}} == teams_topics_tutors

# @pytest.mark.unit
# def test_more_groups_than_topics_but_tutors_with_enough_capacity():
#     """Testing all groups are assigned to one topic when there are more groups than
#     topics but tutors with enough capacities."""
#     group_costs = [
#         [1],
#         [4],
#     ]
#     tutors_capacities = [1, 1]
#     topics_tutors_capacities = [[1], [1]]
#     topics_tutors_costs = [[1], [1]]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(1)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert len(groups.items()) == 2

# @pytest.mark.unit
# def test_more_groups_but_tutor_with_enough_capacity():
#     """Testing all groups are assigned to one topic when there are more groups than
#     topics and tutors but tutor with enough capacity."""
#     group_costs = [
#         [1],
#         [4],
#     ]
#     tutors_capacities = [2]
#     topics_tutors_capacities = [
#         [2],
#     ]
#     topics_tutors_costs = [
#         [1],
#     ]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(1)
#     tutors = create_tutors(
#         1, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert len(groups.items()) == 2

# @pytest.mark.unit
# def test_more_topics_than_groups_and_one_topic_is_assigned_to_each_team():
#     """Testing only one topic is assigned to every team when there are more groups than
#     topics."""
#     group_costs = [
#         [1, 2, 1, 2],
#         [1, 2, 1, 2],
#     ]
#     tutors_capacities = [2, 2]
#     topics_tutors_capacities = [
#         [1, 0, 1, 0],
#         [0, 1, 1, 0],
#     ]
#     topics_tutors_costs = [
#         [1, 1, 1, 1],
#         [1, 1, 1, 1],
#     ]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(4)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     all_topics = ["t1", "t2", "t3", "t4"]
#     all_topics.remove(groups["g1"])
#     all_topics.remove(groups["g2"])
#     not_assigned_topics = all_topics
#     assert len(not_assigned_topics) > 0

# @pytest.mark.unit
# def test_groups_with_same_preferences_and_tutors_with_capacity():
#     """Testing groups with same preferences and costs are assigned to the same topic
#     since it is assigned to tutors that has enough capacity."""
#     group_costs = [
#         [1, 2],
#         [1, 2],
#     ]
#     tutors_capacities = [1, 1]
#     topics_tutors_capacities = [
#         [1, 1],
#         [1, 1],
#     ]
#     topics_tutors_costs = [
#         [1, 1],
#         [1, 1],
#     ]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(2)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert groups["g1"] == groups["g2"]

# @pytest.mark.unit
# def test_groups_with_same_preferences_but_tutor_capacity_not_enough():
#     """Testing groups with same preferences and costs are not assigned
#     to the same topic which is assigned to only one tutor and this
#     tutor does not have enough capacity."""
#     group_costs = [
#         [1, 2],
#         [1, 2],
#     ]
#     tutors_capacities = [1, 1]
#     topics_tutors_capacities = [
#         [1, 0],
#         [0, 1],
#     ]
#     topics_tutors_costs = [
#         [1, 1],
#         [1, 1],
#     ]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(2)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert groups["g1"] != groups["g2"]

# @pytest.mark.unit
# def test_two_groups_with_different_preferences():
#     """Testing two groups with different preferences and can not be assigned
#     a topic with low preference."""
#     group_costs = [
#         [1, 2, 3],  # g1 preferences: t1, t2, t3
#         [2, 1, 3],  # g2 preferences: t2, t1, t3
#     ]
#     tutors_capacities = [1, 1]
#     topics_tutors_capacities = [
#         [1, 1, 1],
#         [1, 1, 1],
#     ]
#     topics_tutors_costs = [
#         [1, 1, 1],
#         [1, 1, 1],
#     ]

#     groups = create_groups(2, group_costs)
#     topics = create_topics(3)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert groups["g1"] == "t1"
#     assert groups["g2"] == "t2"

# @pytest.mark.unit
# def test_more_groups_with_different_preferences():
#     """Testing a team can not be assigned a topic with low preference if the topic that
#     it was chosen is available."""
#     group_costs = [
#         [1, 2, 3],  # g1 preferences: t1, t2, t3
#         [2, 1, 3],  # g2 preferences: t2, t1, t3
#         [3, 2, 1],  # g3 preferences: t3, t2, t1
#     ]
#     tutors_capacities = [2, 1]
#     topics_tutors_capacities = [
#         [1, 1, 1],
#         [1, 1, 1],
#     ]
#     topics_tutors_costs = [
#         [1, 1, 1],
#         [1, 1, 1],
#     ]

#     groups = create_groups(3, group_costs)
#     topics = create_topics(3)
#     tutors = create_tutors(
#         2, tutors_capacities, topics_tutors_capacities, topics_tutors_costs
#     )
#     solver = TopicTutorAssignmentFlowSolver(groups, topics, tutors)
#     groups, _topics, _tutors = solver.solve()
#     assert groups["g1"] == "t1"
#     assert groups["g2"] == "t2"
#     assert groups["g3"] == "t3"

