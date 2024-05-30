"""Module providing helpers function to create different use cases for testing."""

import numpy as np
from src.constants import GROUP_ID, TOPIC_ID, TUTOR_ID
from src.model.group.initial_state_group import InitialStateGroup
from src.model.tutor.initial_state_tutor import InitialStateTutor
from src.model.topic import Topic


class TestHelper:

    def create_topics_for_groups(costs: list):
        """
        Creates a dict of topics with its given costs assigned by the group.

        Args:
            - costs: list of topics costs assigned by the group ordered by topic id.

        Returns a dict of topics with their ids as keys ans its costs as values.
        """
        return {
            Topic(f"{TOPIC_ID}{i}"): topic_cost for i, topic_cost in enumerate(costs)
        }

    def create_groups(self, num_groups: int, topics):
        """
        Creates a list of groups.

        Args:
            - num_groups: number of groups to create.
            - topics: matrix of topics associated with each group.
                     Rows represents groups and columns represents topics.

        Returns: a list of groups with their ids and topics ordered by preference.
        """
        return [
            InitialStateGroup(f"{GROUP_ID}{i}", topics[i - 1])
            for i in range(1, num_groups + 1)
        ]

    def create_topics(self, num_topics: int):
        """
        Creates a list of topics.

        Args:
            - num_topics: number of topics to create.

        Returns: a list of topics with their ids.
        """
        return [Topic(f"{TOPIC_ID}{i}") for i in range(1, num_topics + 1)]

    def create_tutors(
        self, num_tutors: int, group_capacities: list, topics_capacities, topics_costs
    ):
        """
        Creates a list of tutors.

        Args:
            - num_tutors: number of tutors to create.
            - group_capacities: list of number of groups a tutor can take per topic.
            - topics_capacities: matrix indicating the number of topics each tutor
                                 can handle. Rows represents tutors and columns
                                 represents topics.
            - topics_costs: matrix of costs associated with each topic for
                            each tutor. Rows represents tutors and columns
                            represents topics.

        Returns: a list of tutors with their ids, group capacities, and topics
        capacities and costs.
        """
        return [
            InitialStateTutor(
                f"{TUTOR_ID}{i}",
                group_capacities[i - 1],
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

    def get_tutors_groups(self, result):
        """
        Constructs a dictionary with tutors as keys and the groups assigned to
        each tutor as values.

        Args:
            result (list of tuples): The standardized result containing tuples
            (group, topic, tutor).

        Returns a dictionary where keys are tutors and values are lists of
        groups assigned to each tutor.
        """
        tutors_assignments = {}
        for group, topic, tutor in result:
            if tutor not in tutors_assignments:
                tutors_assignments[tutor] = []
            tutors_assignments[tutor].append(group)
        return tutors_assignments

    def get_groups_topics(self, result):
        """
        Constructs a dictionary with groups as keys and the topics assigned
        to each group as values.

        Args:
            result (list of tuples): The standardized result containing tuples
            (group, topic, tutor).

        Returns a dictionary where keys are groups and values are lists of
        topics assigned to each group.
        """
        groups_topics = {}
        for group, topic, tutor in result:
            if group not in groups_topics:
                groups_topics[group] = []
            groups_topics[group].append(topic)
        return groups_topics
