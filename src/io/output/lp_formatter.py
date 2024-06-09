from src.model.utils.result import AssignmentResult
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

    def _create_date(self, assignment: str) -> DeliveryDate:
        # get week, day and hour of date with date-week_id-day_id-hour_id as date id
        date_parts = assignment[2].split("-")
        return DeliveryDate(int(date_parts[1]), int(date_parts[2]), int(date_parts[3]))

    def _id(self, assignment: str, idx: int) -> int:
        return int(assignment[idx].split("-"))

    def _groups(self, result: list[str], groups: list[Group]) -> list[Group]:
        for group in groups:
            for assignment in result:
                # get number_id of group with group-number_id as group id
                group_id = int(assignment[0].split("-")[1])
                if group.id == group_id:
                    date = self._create_date(assignment)
                    group.assign_date(date)
        return groups

    def _evaluators(
        self, result: list[str], evaluators: list[Evaluator]
    ) -> list[Evaluator]:
        for evaluator in evaluators:
            for assignment in result:
                # get number_id of evaluator with evaluator-number_id as evaluator id
                evaluator_id = int(assignment[1].split("-")[1])
                if evaluator.id == evaluator_id:
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