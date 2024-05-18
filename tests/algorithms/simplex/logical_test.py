"""Module testing logical of simplex algorithm."""

from src.algorithms.simplex_solver import SimplexSolver
from tests.algorithms.simplex.helper import (
    create_vector,
    get_all_entities,
    get_teams_topics,
    get_topics,
    get_topics_tutors,
)
import pytest


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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

    # Improve assert to be more accurate and avoid edge cases
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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

    # Improve assert to be more accurate and avoid edge cases
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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

    # Improve assert to be more accurate and avoid edge cases
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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

    # Improve assert to be more accurate and avoid edge cases
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
    topic_tutor = get_topics_tutors(
        topics, tutors, tutor_capacities
    )  # pylint: disable=line-too-long
    topics_c = get_topics(topics, topic_capacities)

    solver = SimplexSolver(None, team_topic, topic_tutor, None)
    teams_topics_tutors = solver.solve_simplex(
        team_topic, topic_tutor, topics_c
    )  # Run the optimization

    # Improve assert to be more accurate and avoid edge cases
    assert {1: {"t2": "p2"}, 2: {"t1": "p1"}, 3: {"t3": "p3"}} == teams_topics_tutors
