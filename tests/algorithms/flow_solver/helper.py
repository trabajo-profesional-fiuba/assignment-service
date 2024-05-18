"""Module providing helpers function to create different use cases for testing."""

import numpy as np
from constants import GROUP_ID, TOPIC_ID, TUTOR_ID
from src.model.group import Group
from src.model.tutor import Tutor
from src.model.topic import Topic


class TestHelper:

    def create_groups(self, num_groups: int, costs):
        """
        Creates a list of groups.

        Args:
            - num_groups: number of groups to create.
            - costs: matrix of costs associated with each group for each topic.
                     Rows represents groups and columns represents topics.

        Returns: a list of groups with their ids and costs.
        """
        return [Group(f"{GROUP_ID}{i}", costs[i - 1]) for i in range(1, num_groups + 1)]

    def create_topics(self, num_topics: int):
        """
        Creates a list of topics.

        Args:
            - num_topics: number of topics to create.

        Returns: a list of topics with their ids.
        """
        return [Topic(f"{TOPIC_ID}{i}") for i in range(1, num_topics + 1)]

    def create_tutors(
        self, num_tutors: int, team_capacities: list, topics_capacities, topics_costs
    ):
        """
        Creates a list of tutors.

        Args:
            - num_tutors: number of tutors to create.
            - team_capacities: list of number of teams a tutor can take per topic.
            - topics_capacities: matrix indicating the number of topics each tutor
                                 can handle. Rows represents tutors and columns
                                 represents topics.
            - topics_costs: matrix of costs associated with each topic for
                            each tutor. Rows represents tutors and columns
                            represents topics.

        Returns: a list of tutors with their ids, team capacities, and topics
        capacities and costs.
        """
        return [
            Tutor(
                f"{TUTOR_ID}{i}",
                team_capacities[i - 1],
                {"capacities": topics_capacities[i - 1], "costs": topics_costs[i - 1]},
            )
            for i in range(1, num_tutors + 1)
        ]

    def create_matrix(self, rows: int, columns: int, is_cost: bool, def_value: int):
        """
        Creates a random cost matrix.

        Args:
            - rows: number of rows to create.
            - columns: number of columns to create.
            - is_cost: indicates is the matrix is a costs matrix.
                       A cost matrix must have 1, 2, 3 somewhere in each row.
            - def_value: value to be set in all cells.
        """
        # Set all values in default value
        matrix = np.full((rows, columns), def_value)
        if is_cost:
            for row in range(rows):
                # Select a random column
                random_col = np.random.randint(columns)
                # Set randomly 1, 2 o 3 in that column
                matrix[row, random_col] = np.random.choice([1, 2, 3])
        return matrix

    def create_list(self, length: int, def_value: int):
        """
        Creates a capacity list.

        Args:
            - length: length of the list.
            - def_value: value to be set in each element of the list.

        Returns a list with default value set in each element of the list.
        """
        # Set all values in default value
        vector = np.full(length, def_value)
        return vector
