import numpy as np

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

def create_matrix(rows: int, columns: int, is_weight: bool, def_value: int):
    """Creates a random weight matrix"""
    matrix = np.full((rows, columns), def_value)  # Set all values in default value
    if is_weight:
        for row in range(rows):
            random_col = np.random.randint(columns)  # Select a random column
            matrix[row, random_col] = np.random.choice([1, 2, 3])  # Set randomly 1, 2 o 3 in that column
    return matrix

def create_vector(columns: int, def_value: int):
    """Creates a random capacity vector with all values in default value."""
    vector = np.full(columns, def_value)  # Set all values in default value
    return vector
