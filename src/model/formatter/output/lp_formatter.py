from typing import Tuple
from src.model.result import AssignmentResult
from src.model.group.group import Group
from src.model.utils.delivery_date import DeliveryDate
from src.model.utils.evaluator import Evaluator


class LPOutputFormatter:
    """
    Formats the output of a linear programming algorithm into a standardized structure.
    """

    def __init__(self) -> None:
        """
        Initializes a `LPOutputFormatter` object.
        """
        pass

    def _create_date(self, assignment: Tuple) -> DeliveryDate:
        return DeliveryDate(assignment[2], assignment[3], assignment[4])

    def _groups(self, result: list[str], groups: list[Group]) -> list[Group]:
        for group in groups:
            for assignment in result:
                if group.id == assignment[0]:
                    date = self._create_date(assignment)
                    group.assign_date(date)
        return groups

    def _evaluators(
        self, result: list[str], evaluators: list[Evaluator]
    ) -> list[Evaluator]:
        for evaluator in evaluators:
            for assignment in result:
                if evaluator.id == assignment[1]:
                    date = self._create_date(assignment)
                    evaluator.assign_date(date)
        return evaluators

    def get_result(
        self, result: list[str], groups: list[Group], evaluators: list[Evaluator]
    ) -> AssignmentResult:
        """
        Formats the simplex algorithm result into a standardized structure.

        Args:
            result (list[str]): The list of strings representing assignments.

        Returns:
            AssignmentResult: An objects with groups.
        """
        return AssignmentResult(
            self._groups(result, groups), self._evaluators(result, evaluators)
        )
