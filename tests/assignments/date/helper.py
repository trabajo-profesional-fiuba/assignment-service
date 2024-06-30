"""Module providing helpers function to create different use cases for testing."""

from src.model.group import Group
from src.model.tutor import Tutor
from src.model.utils.delivery_date import DeliveryDate


class TestLPHelper:

    def create_groups(self, num_groups: int, available_dates: list):
        """
        Creates a list of groups.

        Args:
            - num_groups: number of groups to create.
            - available_dates: dates where the group is available
        Returns: a list of groups with their ids and available dates.
        """
        groups = []
        for i in range(1, num_groups + 1):
            tutor = Tutor((i % 4) + 1, "email", "name")
            tutor.add_available_dates(available_dates)
            groups.append(Group(i, tutor))

        for group in groups:
            group.add_available_dates(available_dates)

        return groups

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
                    date = DeliveryDate(day=day, week=week, hour=hour)
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
        tutors = []
        for i in range(1, num_tutors + 1):
            tutor = Tutor(i, "email", "name")
            tutor.add_available_dates(available_dates)
            tutors.append(tutor)
        return tutors

#    def create_evaluators(self, num_tutors: int, available_dates: list):
#        """
#        Creates a list of evaluators.
#
#        Args:
#            - num_evaluators: number of evaluators to create.
#            - available_dates: dates where the tutor is available
#
#        Returns: a list of evaluators with their with their ids and available dates.
#        """
#        return [
#            Evaluator(
#                i,
#                available_dates,
#            )
#            for i in range(10, num_tutors + 10)
#        ]
