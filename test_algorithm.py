"""Module testing max flow min cost algorithm results."""
from algorithm import run_algorithm

def create_edges(num_groups, num_topics, num_tutors, group_capacities, group_weights,
                 tutor_capacities, tutor_weights, topic_capacities, topic_weights):
    """Creates edges."""

    # Define groups, topics, and tutors
    groups = [f"g{i}" for i in range(1, num_groups + 1)]
    topics = [f"t{j}" for j in range(1, num_topics + 1)]
    tutors = [f"p{k}" for k in range(1, num_tutors + 1)]

    # Define edges from groups to topics
    group_topic_edges = []
    for i, group in enumerate(groups):
        for j, topic in enumerate(topics):
            weight = group_weights[i][j]
            group_topic_edges.append((group, topic,
                                      {"capacity": group_capacities[i], "weight": weight}))

    # Define edges from source to groups
    source_group_edges = [("s", group, {"capacity": 1, "weight": 1}) for group in groups]

    # Define edges from topics to tutors
    topic_tutor_edges = []
    for j, tutor in enumerate(tutors):
        for k, topic in enumerate(topics):
            capacity = topic_capacities[j][k]
            weight = topic_weights[j][k]
            if (capacity > 0 and weight > 0):
                topic_tutor_edges.append((topic, tutor, {"capacity": capacity, "weight": weight}))

    # Define edges from tutors to sink
    tutor_sink_edges = [(tutor, "t", {"capacity": tutor_capacities[i],
                        "weight": tutor_weights[i]}) for i, tutor in enumerate(tutors)]

    # Combine all edges into one list
    all_edges = group_topic_edges + source_group_edges + topic_tutor_edges + tutor_sink_edges

    return all_edges

def test_01_more_teams_than_tutors_without_enough_capacity_but_tutors_do_not_exceed_their_capacities():
    """Testing that not every team is assigned to a tutor if they do not have enough capacity."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    group_capacities = [1, 1, 1]
    group_weights = [
       [1, 2, 3, 4, 4, 4],
       [4, 4, 4, 1, 2, 3],
       [1, 4, 2, 4, 3, 4]
    ]
    tutor_capacities = [1, 1]  # Capacities of tutors p1 and p2
    tutor_weights = [1, 1]     # Weights of tutors p1 and p2
    topic_capacities = [
       [3, 3, 0, 0, 0, 0],  # Capacities of topics for tutor p1
       [0, 0, 3, 3, 3, 3]   # Capacities of topics for tutor p2
    ]
    topic_weights = [
       [1, 1, 0, 0, 0, 0],  # Weights of topics for tutor p1
       [0, 0, 1, 1, 1, 1]   # Weights of topics for tutor p2
    ]
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    _teams, _topics, tutors = run_algorithm(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 1

def test_02_more_teams_than_tutors_but_with_enough_capacity_but_tutors_do_not_exceed_their_capacities():
    """Testing that teams are distributed in both tutors."""
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

    _teams, _topics, tutors = run_algorithm(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 2

def test_03_equal_teams_and_tutors_but_tutors_do_not_exceed_their_capacities():
    """Testing that teams are distributed in all tutors."""
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

    _teams, _topics, tutors = run_algorithm(edges)
    assert len(tutors["p1"]) <= 1
    assert len(tutors["p2"]) <= 1
    assert len(tutors["p3"]) <= 1

def test_03_more_tutors_than_teams_but_tutors_do_not_exceed_their_capacities():
    """Testing that teams are distributed in tutors."""
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

    _teams, _topics, tutors = run_algorithm(edges)
    for tutor, _ in tutors.items():
        assert len(tutors[tutor]) <= 1
