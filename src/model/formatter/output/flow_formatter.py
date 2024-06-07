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
        pass

    def _create_date(self, date: str) -> DeliveryDate:
        """
        Converts a date string into a DeliveryDate object.

        Args:
            date (str): The date string to convert. Expected format is "date-x-x-x".

        Returns:
            DeliveryDate: A `DeliveryDate` object created from the input string.

        Raises:
            WrongDateFormat: If the date string does not match the expected format.
        """
        date_parts = date.split("-")
        if len(date_parts) == 4:
            return DeliveryDate(date_parts[1], date_parts[2], date_parts[3])
        raise WrongDateFormat("Unrecognized date format")

    def _groups(
        self, result: dict[str, dict[str, int]], groups: list[Group]
    ) -> list[Group]:
        """
        Processes groups and assigns delivery dates based on the result dictionary.

        Args:
            result (dict[str, dict[str, int]]): The result dictionary from the flow algorithm.
            groups (list[Group]): List of groups to be processed.

        Returns:
            list[Group]: The list of groups with assigned delivery dates.
        """
        for group in groups:
            if result and groups:
                group_edges = result[f"{GROUP_ID}-{group.id}"]
                for key, value in group_edges.items():
                    if value == 1:
                        date = self._create_date(key)
                        group.assign_date(date)
        return groups

    def get_result(
        self,
        result: dict[str, dict[str, int]],
        groups: list[Group],
        evaluators: list[Evaluator],
    ) -> AssignmentResult:
        """
        Formats the flow algorithm result into a standardized structure.

        Args:
            result (dict[str, dict[str, int]]): The result dictionary from the flow algorithm.
            groups (list[Group]): List of groups with tutors to be assigned a delivery date.
            evaluators (list[Evaluator]): List of evaluators.

        Returns:
            AssignmentResult: An object with groups and evaluators.
        """
        return AssignmentResult(self._groups(result, groups), evaluators)
