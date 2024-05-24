"""Module testing logic, performance and scalability of max flow min cost algorithm
when assigning topics and tutors to groups."""

import pytest
import time

from src.algorithms.simplex.tutor_topics import TopicTutorAssignmentSimplexSolver
from tests.algorithms.simplex.helper import (
    create_vector,
    get_all_entities,
    get_teams_topics,
    get_topics_tutors,
    get_topics,
)


# ------------ Logic Tests ------------
@pytest.mark.unit
def test_more_teams_than_tutors_without_enough_capacity():
    """Testing that tutors dont get all teams so they not to exceed their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    assert len(teams_topics_tutors.items()) == 2


@pytest.mark.unit
def test_more_teams_than_tutors_but_with_enough_capacity_all_teams_are_assigned():
    """Testing that tutors get all teams without exceeding their capacities."""
    num_groups = 3
    num_topics = 6
    num_tutors = 2
    tutor_capacities = [1, 2]
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
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
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    assert len(teams_topics_tutors.items()) == 3


@pytest.mark.unit
def test_more_tutors_than_groups_tutors_dont_exceed_their_capacities():
    num_groups = 3
    num_topics = 6
    num_tutors = 6
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    assert {1: {"t1": "p2"}, 2: {"t2": "p1"}, 3: {"t3": "p4"}} == teams_topics_tutors


@pytest.mark.unit
def test_more_groups_than_topics_but_tutors_with_enough_capacity():
    """Testing all groups are assigned to one topic when there are more groups than
    topics but tutors with enough capacities."""
    num_groups = 3
    num_topics = 1
    num_tutors = 3
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(1, 3)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    assert {1: {"t1": "p2"}, 2: {"t1": "p3"}, 3: {"t1": "p1"}} == teams_topics_tutors


@pytest.mark.unit
def test_more_topics_than_groups_and_one_topic_is_assigned_to_each_team():
    """Testing only one topic is assigned to every team when there are more groups than
    topics."""
    num_groups = 3
    num_topics = 4
    num_tutors = 3
    tutor_capacities = create_vector(num_tutors, 1)
    topic_capacities = create_vector(num_topics, 1)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    assert {1: {"t2": "p2"}, 2: {"t1": "p1"}, 3: {"t3": "p3"}} == teams_topics_tutors


# ------------ Performance and Scalability Tests ------------
@pytest.mark.performance
def test_four_teams_and_topics():
    """Testing if the algorithm is overhead with four teams and topics."""
    num_groups = 4
    num_topics = 4
    num_tutors = 2
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print(
        "[simplex solver]: 4 groups, 4 topics, 2 tutors - Execution time:",
        end_time - start_time,
        "seconds",
    )


@pytest.mark.performance
def test_ten_teams_and_topics():
    """Testing if the algorithm is overhead with ten teams and topics."""
    num_groups = 10
    num_topics = 10
    num_tutors = 5
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print(
        "[simplex solver]: 10 groups, 10 topics, 5 tutors - Execution time:",
        end_time - start_time,
        "seconds",
    )


@pytest.mark.performance
def test_twenty_teams_and_topics():
    """Testing if the algorithm is overhead with twenty teams and topics."""
    num_groups = 20
    num_topics = 20
    num_tutors = 10
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print(
        "[simplex solver]: 20 groups, 20 topics, 10 tutors - Execution time:",
        end_time - start_time,
        "seconds",
    )


@pytest.mark.performance
def test_test_forty_teams_and_topics():
    """Testing if the algorithm is overhead with forty teams and topics."""
    num_groups = 40
    num_topics = 40
    num_tutors = 20
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)
    start_time = time.time()
    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print(
        "[simplex solver]: 40 groups, 40 topics, 20 tutors - Execution time:",
        end_time - start_time,
        "seconds",
    )


@pytest.mark.performance
def test_eighty_teams_and_topics():
    """Testing if the algorithm is overhead with eighty teams and topics."""
    num_groups = 80
    num_topics = 80
    num_tutors = 40
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(topics, tutors, tutor_capacities)
    topics_c = get_topics(topics, topic_capacities)
    start_time = time.time()
    solver = TopicTutorAssignmentSimplexSolver(team_topic, topic_tutor, topics_c)
    teams_topics_tutors = solver.solve_simplex()
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print(
        "[simplex solver]: 80 groups, 80 topics, 4 tutors - Execution time:",
        end_time - start_time,
        "seconds",
    )
