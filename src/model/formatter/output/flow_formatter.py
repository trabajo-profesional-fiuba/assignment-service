from src.constants import GROUP_ID
from src.model.group.group import Group
from src.model.result import AssignmentResult
from src.model.utils.evaluator import Evaluator
from src.model.utils.delivery_date import DeliveryDate
from src.exceptions import WrongDateFormat


class FlowOutputFormatter:
    """
    Formats the output of a flow algorithm into a standardized structure.
    """

    def __init__(self) -> None:
        """
        Initializes a `FlowOutputFormatter` object.
        """

    def _create_date(self, date: str) -> DeliveryDate:
        date_parts = date.split("-")
        if len(date_parts) == 4:
            return DeliveryDate(date_parts[1], date_parts[2], date_parts[3])
        raise WrongDateFormat("Unrecognized date format")

    def _groups(
        self, result: dict[str, dict[str, int]], groups: list[Group]
    ) -> list[Group]:
        for group in groups:
            group_edges = result[f"{GROUP_ID}-{group.id}"]
            for key, value in group_edges.items():
                if value == 1:
                    group.assign_date(key)
        return groups

    def get_result(
        self,
        result: dict[str, dict[str, int]],
        groups: list[Group],
        evaluators: list[Evaluator],
    ) -> AssignmentResult:
        """
        Formats the flow algorithm result into a standardized structure.

        Processes the result dictionary and extracts assignments where the value is 1,
        and adds them to the standardized result as AssignmentResult.

        Args:
            - result (dict[str, dict[str, int]]): The result dictionary from the flow
            algorithm.
            - groups (list[Group]): List of groups with tutors to be assigned
            a delivery date.
            - evaluators (list[Evaluator]): List of evaluators to be assigned
            a delivery date.

        Returns:
            AssignmentResult: An object with groups.
        """
        return AssignmentResult(self._groups(result, groups), evaluators)
