"""Module testing logical of max flow min cost algorithm."""
from test.max_flow_min_cost.helper import create_edges
from algorithm import max_flow_min_cost

def test_more_teams_than_tutors_without_enough_capacity_so_there_are_teams_without_tutor():
    """Testing that tutors do not get all teams in order not to exceed their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    group_capacities = [1, 1, 1]
    group_weights = [
       [1, 2, 3, 4, 4, 4], # teams as rows
       [4, 4, 4, 1, 2, 3], # topics as columns
       [1, 4, 2, 4, 3, 4]
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [3, 3, 0, 0, 0, 0],  # tutors as rows
       [0, 0, 3, 3, 3, 3]   # topics as columns
    ]
    topic_weights = [
       [1, 1, 0, 0, 0, 0],  # tutors as rows
       [0, 0, 1, 1, 1, 1]   # topics as columns
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    _teams, _topics, tutors = max_flow_min_cost(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 1

def test_more_teams_than_tutors_but_with_enough_capacity_so_all_teams_are_assigned_to_a_tutor():
    """Testing that tutors get all teams without exceeding their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    group_capacities = [1, 1, 1]
    group_weights = [
       [1, 2, 3, 4, 4, 4],
       [4, 4, 4, 1, 2, 3],
       [1, 4, 2, 4, 3, 4]
    ]
    tutor_capacities = [1, 2]
    tutor_weights = [1, 1]
    topic_capacities = [
       [3, 3, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3]
    ]
    topic_weights = [
       [1, 1, 0, 0, 0, 0],
       [0, 0, 1, 1, 1, 1]
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    _teams, _topics, tutors = max_flow_min_cost(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 2

def test_equal_teams_and_tutors_but_tutors_do_not_exceed_their_capacities():
    """Testing that tutors get all teams without exceeding their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 3
    group_capacities = [1, 1, 1]
    group_weights = [
       [1, 2, 3, 4, 4, 4],
       [4, 4, 4, 1, 2, 3],
       [1, 4, 2, 4, 3, 4]
    ]
    tutor_capacities = [1, 1, 1]
    tutor_weights = [1, 1, 1]
    topic_capacities = [
       [3, 3, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3],
       [0, 0, 3, 3, 3, 3]
    ]
    topic_weights = [
       [1, 1, 0, 0, 0, 0],
       [0, 0, 1, 1, 1, 1],
       [0, 0, 1, 1, 1, 1]
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    _teams, _topics, tutors = max_flow_min_cost(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 1
    assert len(tutors["p3"]) <= 1

def test_more_tutors_than_teams_but_tutors_do_not_exceed_their_capacities():
    """Testing that teams are distributed between tutors in order not to exceed their capacities."""
    num_groups = 2
    num_topics = 6
    num_tutors = 3
    group_capacities = [1, 1]
    group_weights = [
       [1, 2, 3, 4, 4, 4],
       [4, 4, 4, 1, 2, 3],
    ]
    tutor_capacities = [1, 1, 1]
    tutor_weights = [1, 1, 1]
    topic_capacities = [
       [3, 3, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3],
       [0, 0, 3, 3, 3, 3]
    ]
    topic_weights = [
       [1, 1, 0, 0, 0, 0],
       [0, 0, 1, 1, 1, 1],
       [0, 0, 1, 1, 1, 1]
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    _teams, _topics, tutors = max_flow_min_cost(edges)
    for tutor, _ in tutors.items():
        assert len(tutors[tutor]) <= 1

def test_equal_teams_and_topics_so_every_team_is_assigned_to_one_topic():
    """Testing all teams are assigned to one topic when there are enough tutors with
    enough capacities."""
    num_groups = 2
    num_topics = 2
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1, 2],
       [4, 4],
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 0],
       [0, 1],
    ]
    topic_weights = [
       [1, 1],
       [1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert len(teams.items()) == 2

def test_more_teams_than_topics_but_tutors_with_enough_capacity_so_every_team_is_assigned_to_one_topic():
    """Testing all teams are assigned to one topic when there are more teams than topics 
    but tutors with enough capacities."""
    num_groups = 2
    num_topics = 1
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1],
       [4],
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1],
       [1]
    ]
    topic_weights = [
       [1],
       [1]
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert len(teams.items()) == 2

def test_more_teams_than_topics_and_tutors_but_tutor_with_enough_capacity_so_every_team_is_assigned_to_one_topic():
    """Testing all teams are assigned to one topic when there are more teams than topics and tutors 
    but tutor with enough capacity."""
    num_groups = 2
    num_topics = 1
    num_tutors = 1
    group_capacities = [1, 1]
    group_weights = [
       [1],
       [4],
    ]
    tutor_capacities = [2]
    tutor_weights = [1]
    topic_capacities = [
       [2],
    ]
    topic_weights = [
       [1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert len(teams.items()) == 2

def test_more_topics_than_teams_but_just_one_topic_is_assigned_to_each_team():
    """Testing only one topic is assigned to every team when there are more teams than topics."""
    num_groups = 2
    num_topics = 4
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1, 2, 1, 2],
       [1, 2, 1, 2],
    ]
    tutor_capacities = [2, 2]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 0, 1, 0],
       [0, 1, 1, 0],
    ]
    topic_weights = [
       [1, 1, 1, 1],
       [1, 1, 1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    all_topics = ["t1", "t2", "t3", "t4"]
    all_topics.remove(teams["g1"])
    all_topics.remove(teams["g2"])
    not_assigned_topics = all_topics
    assert len(not_assigned_topics) > 0

def test_teams_with_same_preferences_and_weights_and_tutors_with_capacity_are_assigned_to_the_same_topic():
    """Testing teams with same preferences and weights are assigned to the same topic since 
    it is assigned to tutors that has enough capacity."""
    num_groups = 2
    num_topics = 2
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1, 2],
       [1, 2],
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 1],
       [1, 1],
    ]
    topic_weights = [
       [1, 1],
       [1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert teams["g1"] == teams["g2"]

def test_teams_with_same_preferences_but_tutor_capacity_for_topic_is_not_enough_so_are_not_assigned_to_the_same_topic():
    """Testing teams with same preferences and weights are not assigned to the same topic which 
    is assigned to only one tutor and this tutor does not have enough capacity."""
    num_groups = 2
    num_topics = 2
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1, 2],
       [1, 2],
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 0],
       [0, 1],
    ]
    topic_weights = [
       [1, 1],
       [1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert teams["g1"] != teams["g2"]

def test_two_teams_with_different_preferences_can_not_be_assigned_a_topic_with_low_preference():
    """Testing two teams with different preferences and can not be assigned 
    a topic with low preference."""
    num_groups = 2
    num_topics = 3
    num_tutors = 2
    group_capacities = [1, 1]
    group_weights = [
       [1, 2, 3], # g1 preferences: t1, t2, t3
       [2, 1, 3], # g2 preferences: t2, t1, t3
    ]
    tutor_capacities = [1, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 1, 1],
       [1, 1, 1],
    ]
    topic_weights = [
       [1, 1, 1],
       [1, 1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert teams["g1"] == "t1"
    assert teams["g2"] == "t2"

def test_more_teams_with_different_preferences_can_not_be_assigned_a_topic_with_low_preference():
    """Testing a team can not be assigned a topic with low preference if the topic that
    it was chosen is available."""
    num_groups = 3
    num_topics = 3
    num_tutors = 2
    group_capacities = [1, 1, 1]
    group_weights = [
       [1, 2, 3], # g1 preferences: t1, t2, t3
       [2, 1, 3], # g2 preferences: t2, t1, t3
       [3, 2, 1]  # g3 preferences: t3, t2, t1
    ]
    tutor_capacities = [2, 1]
    tutor_weights = [1, 1]
    topic_capacities = [
       [1, 1, 1],
       [1, 1, 1],
    ]
    topic_weights = [
       [1, 1, 1],
       [1, 1, 1],
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    teams, _topics, _tutors = max_flow_min_cost(edges)
    assert teams["g1"] == "t1"
    assert teams["g2"] == "t2"
    assert teams["g3"] == "t3"
    