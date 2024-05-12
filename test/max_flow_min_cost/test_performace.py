"""Module testing performance and scalability of max flow min cost algorithm."""
import time
from test.max_flow_min_cost.helper import create_edges, create_matrix, create_vector
from algorithm import max_flow_min_cost

def test_four_teams_and_topics():
    """Testing if the algorithm is overhead with four teams and topics."""
    num_groups = 4
    num_topics = 4
    num_tutors = 2
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 01 - Execution time:", end_time - start_time, "seconds")

def test_ten_teams_and_topics():
    """Testing if the algorithm is overhead with ten teams and topics."""
    num_groups = 10
    num_topics = 10
    num_tutors = 5
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 02 - Execution time:", end_time - start_time, "seconds")

def test_twenty_teams_and_topics():
    """Testing if the algorithm is overhead with twenty teams and topics."""
    num_groups = 20
    num_topics = 20
    num_tutors = 10
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 03 - Execution time:", end_time - start_time, "seconds")

def test_forty_teams_and_topics():
    """Testing if the algorithm is overhead with forty teams and topics."""
    num_groups = 40
    num_topics = 40
    num_tutors = 20
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 04 - Execution time:", end_time - start_time, "seconds")

def test_eighty_teams_and_topics():
    """Testing if the algorithm is overhead with eighty teams and topics."""
    num_groups = 80
    num_topics = 80
    num_tutors = 40
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 05 - Execution time:", end_time - start_time, "seconds")

def test_one_hundred_and_sixty_teams_and_topics():
    """Testing if the algorithm is overhead with one hundred and sixty teams and topics."""
    num_groups = 160
    num_topics = 160
    num_tutors = 80
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 06 - Execution time:", end_time - start_time, "seconds")

def test_three_hundred_and_twenty_teams_and_topics():
    """Testing if the algorithm is overhead with three hundred and twenty teams and topics."""
    num_groups = 320
    num_topics = 320
    num_tutors = 160
    group_capacities = create_vector(num_groups, 1)
    group_weights = create_matrix(num_groups, num_topics, True, 4)
    tutor_capacities = create_vector(num_groups, 2)
    tutor_weights = create_vector(num_groups, 1)
    topic_capacities = create_matrix(num_tutors, num_topics, False, 2)
    topic_weights = create_matrix(num_tutors, num_topics, False, 1)
    edges = create_edges(num_groups, num_topics, num_tutors, group_capacities,
                group_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights)

    start_time = time.time()
    teams, _topics, _tutors = max_flow_min_cost(edges)
    end_time = time.time()
    assert len(teams.items()) > 0
    print("Test 07 - Execution time:", end_time - start_time, "seconds")
