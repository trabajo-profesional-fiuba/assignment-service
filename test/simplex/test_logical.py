"""Module testing logical of simplex algorithm."""
from src.algorithms.simplex_solver import SimplexSolver
from test.simplex.helper import create_vector, get_all_entities, get_teams_topics, get_topics, get_topics_tutors

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