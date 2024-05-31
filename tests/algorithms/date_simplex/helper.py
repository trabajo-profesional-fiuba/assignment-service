"""Module providing helpers function to create different use cases for testing."""

from src.model.group.final_state_group import FinalStateGroup
from src.model.tutor.final_state_tutor import FinalStateTutor
from src.model.utils.date_dto import DateDto
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
            FinalStateGroup((f"g{i}"), available_dates, (f"t{(i % 4)+1}"))
            for i in range(1, num_groups + 1)
        ]

    def create_dates(self, num_weeks: int, days_per_week: list, hours_per_day: list):
        """
        Creates a list of dates.

        Args:
            - num_weeks: number of weeks to create dates for.
            - days_per_week: list of days in a week (e.g., ["Monday", "Tuesday", ...]).
            - hours_per_day: list of hours in a day (instances of Hour enum).

        Returns: a list of Date objects.
        """
        dates = []
        for week in range(1, num_weeks + 1):
            for day in days_per_week:
                for hour in hours_per_day:
                    date = DateDto(day=day, week=week, hr=hour)
                    dates.append(date)
        return dates

    def create_tutors(self, num_tutors: int, available_dates: list):
        """
        Creates a list of tutors.

        Args:
            - num_tutors: number of tutors to create.
            - available_dates: dates where the tutor is available

        Returns: a list of tutors with their with their ids and available dates.
        """
        return [
            FinalStateTutor(
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
