"""Module providing helpers function to create different use cases for testing."""

import numpy as np
from constants import GROUP_ID, TOPIC_ID, TUTOR_ID
from src.model.group import Group
from src.model.tutor import Tutor
from src.model.topic import Topic


def create_groups(num_groups: int, costs):
    return [Group(f"{GROUP_ID}{i}", costs[i - 1]) for i in range(1, num_groups + 1)]


def create_topics(num_topics: int):
    return [Topic(f"{TOPIC_ID}{i}") for i in range(1, num_topics + 1)]


def create_tutors(
    num_tutors: int, team_capacities: list, topics_capacities, topics_costs
):
    return [
        Tutor(
            f"{TUTOR_ID}{i}",
            team_capacities[i - 1],
            {"capacities": topics_capacities[i - 1], "costs": topics_costs[i - 1]},
        )
        for i in range(1, num_tutors + 1)
    ]


def create_matrix(rows: int, columns: int, is_cost: bool, def_value: int):
    """Creates a random cost matrix"""
    matrix = np.full((rows, columns), def_value)  # Set all values in default value
    if is_cost:
        for row in range(rows):
            random_col = np.random.randint(columns)  # Select a random column
            # Set randomly 1, 2 o 3 in that column
            matrix[row, random_col] = np.random.choice([1, 2, 3])
    return matrix


def create_vector(columns: int, def_value: int):
    """Creates a random capacity vector with all values in default value."""
    vector = np.full(columns, def_value)  # Set all values in default value
    return vector
