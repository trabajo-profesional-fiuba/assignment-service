import time

from src.algorithms.simplex_solver import SimplexSolver
from tests.algorithms.simplex.helper import (
    create_vector,
    get_all_entities,
    get_teams_topics,
    get_topics,
    get_topics_tutors,
)
import pytest


@pytest.mark.performance
def test_01_four_teams_and_topics():
    """Testing if the algorithm is overhead with four teams and topics."""
    num_groups = 4
    num_topics = 4
    num_tutors = 2
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print("[TEST] 01 - Execution time:", end_time - start_time, "seconds")


@pytest.mark.performance
def test_02_ten_teams_and_topics():
    """Testing if the algorithm is overhead with ten teams and topics."""
    num_groups = 10
    num_topics = 10
    num_tutors = 5
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print("[TEST] 02 - Execution time:", end_time - start_time, "seconds")


@pytest.mark.performance
def test_03_twenty_teams_and_topics():
    """Testing if the algorithm is overhead with twenty teams and topics."""
    num_groups = 20
    num_topics = 20
    num_tutors = 10
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    start_time = time.time()
    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print("[TEST] 03 - Execution time:", end_time - start_time, "seconds")


@pytest.mark.performance
def test_04_test_forty_teams_and_topics():
    """Testing if the algorithm is overhead with forty teams and topics."""
    num_groups = 40
    num_topics = 40
    num_tutors = 20
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)
    start_time = time.time()
    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print("[TEST] 04 - Execution time:", end_time - start_time, "seconds")


@pytest.mark.performance
def test_05_eighty_teams_and_topics():
    """Testing if the algorithm is overhead with eighty teams and topics."""
    num_groups = 80
    num_topics = 80
    num_tutors = 40
    tutor_capacities = create_vector(num_groups, 2)
    topic_capacities = create_vector(num_topics, 2)
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)

    team_topic = get_teams_topics(teams, topics)
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)
    start_time = time.time()
    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization
    end_time = time.time()
    assert len(teams_topics_tutors.items()) > 0
    print("[TEST] 05 - Execution time:", end_time - start_time, "seconds")
