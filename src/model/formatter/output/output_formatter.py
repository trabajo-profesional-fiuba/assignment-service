from typing import Union
from src.model.formatter.output.flow_formatter import FlowOutputFormatter
from src.model.formatter.output.lp_formatter import LPOutputFormatter
from src.exceptions import ResultFormatNotFound
from src.model.group.group import Group
from src.model.result import AssignmentResult
from src.model.utils.evaluator import Evaluator


class OutputFormatter:
    """
    Class for formatting assignment algorithm results.

    This class provides a standardized interface for formatting the results
    of the assignment algorithm. It supports different result formats and
    uses the appropriate formatter based on the type of result.
    """

    FORMATTERS = {dict: FlowOutputFormatter(), list: LPOutputFormatter()}

    def __init__(self) -> None:
        """
        Initializes an `OutputFormatter` object.
        """
        pass

    def format_result(
        self,
        result: Union[dict, list],
        groups: list[Group],
        evaluators: list[Evaluator],
    ) -> AssignmentResult:
        """
        Formats the algorithm result into a standardized structure.

        This method automatically detects the type of the result
        (either flow or simplex) and calls the corresponding formatter
        class to process it.

        Args:
            - result (Union[dict, list]): The result of the assignment algorithm,
            which can be of type `dict` or `list`.
            - groups (list[Group]): List of groups with tutors to be assigned a delivery date.
            - evaluators (list[Evaluator]): List of evaluators to be assigned a delivery date.

        Returns:
            AssignmentResult: The formatted result, as processed by the appropriate
            formatter class.

        Raises:
            ResultFormatNotFound: If the result type is not recognized by
            any formatter.
        """
        result_type = type(result)
        formatter = self.FORMATTERS.get(result_type)
        if formatter:
            return formatter.get_result(result, groups, evaluators)
        else:
            raise ResultFormatNotFound("Unrecognized result format")
