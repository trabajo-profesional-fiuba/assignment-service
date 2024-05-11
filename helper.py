"""Module providing helpers function to create different use cases for testing."""

import numpy as np # pylint: disable=E0401

def get_entity(entity_id: str, num_entities: int):
    """Define a group of entities. An entity can be a team, a topic or a tutor."""
    return [f"{entity_id}{i}" for i in range(1, num_entities + 1)]

def get_all_entities(num_teams: int, num_topics: int, num_tutors: int):
    """Define groups, topics, and tutors."""
    teams = get_entity("g", num_teams)
    topics = get_entity("t", num_topics)
    tutors = get_entity("p", num_tutors)
    return teams, topics, tutors

def get_source_teams_edges(teams):
    """Define edges from source to groups."""
    return [("s", team, {"capacity": 1, "weight": 1}) for team in teams]

def get_teams_topics_edges(teams, topics, team_weights, team_capacities: []):
    """Define edges from groups to topics."""
    team_topic_edges = []
    for i, group in enumerate(teams):
        for j, topic in enumerate(topics):
            weight = team_weights[i][j]
            team_topic_edges.append((group, topic,
                {"capacity": team_capacities[i], "weight": weight}))
    return team_topic_edges

def get_topics_tutors_edges(topics, tutors, topic_capacities, topic_weights):
    """Define edges from topics to tutors."""
    topic_tutor_edges = []
    for j, tutor in enumerate(tutors):
        for k, topic in enumerate(topics):
            capacity = topic_capacities[j][k]
            weight = topic_weights[j][k]
            if (capacity > 0 and weight > 0):
                topic_tutor_edges.append((topic, tutor, {"capacity": capacity, "weight": weight}))
    return topic_tutor_edges

def get_tutors_sink_edges(tutors, tutor_capacities, tutor_weights):
    """Define edges from tutors to sink."""
    tutor_sink_edges = [(tutor, "t", {"capacity": tutor_capacities[i],
                        "weight": tutor_weights[i]}) for i, tutor in enumerate(tutors)]
    return tutor_sink_edges

def create_edges(num_groups: int, num_topics: int, num_tutors: int, team_capacities: [],
                 team_weights, tutor_capacities, tutor_weights, topic_capacities, topic_weights):
    """Creates edges to create a digraph. 
    The edges are from source node to teams nodes, from teams
    nodes to topic nodes, from topics nodes to tutors nodes, and from tutors nodes to sink node."""
    teams, topics, tutors = get_all_entities(num_groups, num_topics, num_tutors)
    team_topic_edges = get_teams_topics_edges(teams, topics, team_weights, team_capacities)
    source_teams_edges = get_source_teams_edges(teams)
    topic_tutor_edges = get_topics_tutors_edges(topics, tutors, topic_capacities, topic_weights) # pylint: disable=line-too-long
    tutor_sink_edges = get_tutors_sink_edges(tutors, tutor_capacities, tutor_weights)
    return team_topic_edges + source_teams_edges + topic_tutor_edges + tutor_sink_edges

def create_matrix(rows: int, columns: int, is_weight: bool, def_value: int):
    """Creates a random weight matrix"""
    matrix = np.full((rows, columns), def_value)  # Set all values in default value
    if is_weight:
        for row in range(rows):
            random_col = np.random.randint(columns)  # Select a random column
            # Set randomly 1, 2 o 3 in that column
            matrix[row, random_col] = np.random.choice([1, 2, 3])
    return matrix

def create_vector(columns: int, def_value: int):
    """Creates a random capacity vector with all values in default value."""
    vector = np.full(columns, def_value)  # Set all values in default value
    return vector
