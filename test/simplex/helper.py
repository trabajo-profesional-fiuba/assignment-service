import numpy as np

TEAM_ID = "g"
TOPIC_ID = "t"
TUTOR_ID = "p"

def create_vector(columns: int, def_value: int):
    """Creates a random capacity vector with all values in default value."""
    vector = np.full(columns, def_value)  # Set all values in default value
    return vector

def get_entity(entity_id: str, num_entities: int):
    """Define a group of entities. An entity can be a team, a topic or a tutor."""
    return [f"{entity_id}{i}" for i in range(1, num_entities + 1)]

def get_all_entities(num_teams: int, num_topics: int, num_tutors: int):
    """Define groups, topics, and tutors."""
    teams = get_entity(TEAM_ID, num_teams)
    topics = get_entity(TOPIC_ID, num_topics)
    tutors = get_entity(TUTOR_ID, num_tutors)
    return teams, topics, tutors

def get_teams_topics(teams, topics):
    """Define la unión de grupos a temas."""
    team_topics = []
    for team in teams:
        team_topics.append([team, []])
        for topic in topics:
            team_topics[-1][1].append(topic)
    return team_topics

def get_topics_tutors(topics, tutors, tutor_capacities):
    """Define edges from topics to tutors."""
    topic_tutor = []
    for j, tutor in enumerate(tutors):
        capacity = tutor_capacities[j]
        topic_tutor.append([tutor, {"capacity": capacity}, []])
        for k, topic in enumerate(topics):
            topic_tutor[-1][2].append(topic)
    return topic_tutor

def get_topics(topics, topic_capacities):
    """Define edges from tutors to sink."""
    topics = [(topic, {"capacity": topic_capacities[i]}) for i, topic in enumerate(topics)]
    return topics