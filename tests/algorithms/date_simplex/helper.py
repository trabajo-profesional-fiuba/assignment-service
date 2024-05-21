"""Module providing helpers function to create different use cases for testing."""

from src.model.group.simplex_group import SimplexGroup
from src.model.tutor.simplex_tutor import SimplexTutor
from src.model.utils.evaluator import Evaluator


class TestSimplexHelper:

    def create_groups(self, num_groups: int, available_dates: list):
        """
        Creates a list of groups.

        Args:
            - num_groups: number of groups to create.
            - available_dates: dates where the group is available
        Returns: a list of groups with their ids and available dates.
        """
        return [
            SimplexGroup((f"g{i}"), available_dates, (f"t{(i % 4)+1}"))
            for i in range(1, num_groups + 1)
        ]

    def create_dates(self, num_dates: int):
        """
        Creates a list of dates.

        Args:
            - num_dates: number of dates to create.

        Returns: a list of dates.
        """
        return [(f"date{i}") for i in range(1, num_dates + 1)]

    def create_tutors(self, num_tutors: int, available_dates: list):
        """
        Creates a list of tutors.

        Args:
            - num_tutors: number of tutors to create.
            - available_dates: dates where the tutor is available

        Returns: a list of tutors with their with their ids and available dates.
        """
        return [
            SimplexTutor(
                f"t{i}",
                available_dates,
            )
            for i in range(1, num_tutors + 1)
        ]

    def create_evaluators(self, num_tutors: int, available_dates: list):
        """
        Creates a list of evaluators.

        Args:
            - num_evaluators: number of evaluators to create.
            - available_dates: dates where the tutor is available

        Returns: a list of evaluators with their with their ids and available dates.
        """
        return [
            Evaluator(
                f"e{i}",
                available_dates,
            )
            for i in range(1, num_tutors + 1)
        ]
