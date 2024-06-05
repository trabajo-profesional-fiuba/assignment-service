from typing import Tuple
from src.model.result import AssignmentResult
from src.model.group.group import Group
from src.model.utils.delivery_date import DeliveryDate


class LPOutputFormatter:
    """
    Formats the output of a linear programming algorithm into a standardized structure.
    """

    def __init__(self) -> None:
        """
        Initializes a `LPOutputFormatter` object.
        """
        pass

    def _create_date(assignment: Tuple) -> DeliveryDate:
        return DeliveryDate(assignment[1], assignment[2], assignment[3])

    def _groups(self, result: list[str], groups: list[Group]) -> list[Group]:
        for group in groups:
            for assignment in result:
                if group.id == assignment[0]:
                    date = self._create_date(assignment)
                    group.assign_date(date)
        return groups

    def get_result(self, result: list[str], groups: list[Group]) -> AssignmentResult:
        """
        Formats the simplex algorithm result into a standardized structure.

        Args:
            result (list[str]): The list of strings representing assignments.

        Returns:
            AssignmentResult: An objects with groups.
        """
        # return AssignmentResult(self._groups(result, groups))
        return result
