import numpy as np

from src.constants import TOPIC_ID, TUTOR_ID
from src.model.group import Group
from src.model.group.initial_state_group import InitialStateGroup
from src.model.tutor import Tutor
from src.model.tutor.initial_state_tutor import InitialStateTutor
from src.model.utils.topic import Topic


class TestHelper:

    def _create_topics(
        self, num_topics: int, costs: list[int], capacities: list[int]
    ) -> list[Topic]:
        """
        Creates a list of `Topic`.

        Args:
            - num_topics (int): number of topics to create.
            - costs (list[int]): list of topic costs ordered by topic id.
            - capacities (list[int]): list of topic capacities ordered by topic id.

        Returns (list[Topic]):
            A list of topics with their ids, tittles, costs and capacities.
        """
        return [
            Topic(i, f"{TOPIC_ID}{i}", costs[i - 1], capacities[i - 1])
            for i in range(1, num_topics + 1)
        ]

    def create_groups(
        self,
        num_groups: int,
        num_topics: int,
        topics_costs: list[list[int]],
        topics_capacities: list[int],
    ) -> list[Group]:
        """
        Creates a list of `Group`.

        Args:
            - num_groups (int): number of groups to create.
            - num_topics (int): number of topics to create.
            - topics_costs (list[list[int]]): matrix of topic costs ordered by topic id.
                                            Rows represents groups and columns
                                            represents topics.
            - topics_capacities (list[int]): list of topic capacities ordered by topic
                                            id. Each index + 1 represents the capacity
                                            of the topic id.

        Returns (list[Group]):
            A list of groups with their ids and states.
        """
        return [
            Group(
                i,
                state=InitialStateGroup(
                    self._create_topics(
                        num_topics, topics_costs[i - 1], topics_capacities
                    )
                ),
            )
            for i in range(1, num_groups + 1)
        ]

    def create_tutors(
        self,
        num_tutors: int,
        group_capacities: list[int],
        num_topics: int,
        topics_capacities: list[list[int]],
        topics_costs: list[list[int]],
    ) -> list[Tutor]:
        """
        Creates a list of `Tutor`.

        Args:
            - num_tutors (int): number of tutors to create.
            - group_capacities (list[int]): list of number of groups a tutor can take
                                            per topic.
            - num_topics (int): number of topics to create.
            - topics_capacities (list[list[int]]): matrix indicating the number of
                                topics each tutor can handle. Rows represents tutors and
                                columns represents topics.
            - topics_costs (list[list[int]]): matrix of costs associated with each topic
                            for each tutor. Rows represents tutors and columns
                            represents topics.

        Returns (list[Tutor]):
            A list of tutors with their ids, group capacities, and topics
            capacities and costs.
        """
        return [
            Tutor(
                i,
                f"{TUTOR_ID}{i}@fi.uba.ar",
                f"{TUTOR_ID}{i}",
                state=InitialStateTutor(
                    i,
                    group_capacities[i - 1],
                    self._create_topics(
                        num_topics, topics_costs[i - 1], topics_capacities[i - 1]
                    ),
                ),
            )
            for i in range(1, num_tutors + 1)
        ]

    def create_matrix(
        self, rows: int, columns: int, is_cost: bool, def_value: int
    ) -> list[list[int]]:
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

    def create_list(self, length: int, def_value: int) -> list[int]:
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

    def get_tutors_groups(self, result: tuple[str, str, str]) -> dict[str, str]:
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

    def get_groups_topics(self, result: tuple[str, str, str]) -> dict[str, str]:
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
