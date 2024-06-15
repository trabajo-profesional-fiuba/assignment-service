from typing import Union
from src.io.output.flow_formatter import FlowOutputFormatter
from src.io.output.lp_formatter import LPOutputFormatter
from src.io.output.result_context import ResultContext
from src.exceptions import ResultFormatNotFound
from src.model.group.group import Group
from src.model.utils.result import AssignmentResult
from src.model.utils.evaluator import Evaluator


class OutputFormatter:
    """
    Class for formatting assignment algorithm results.

    This class provides a standardized interface for formatting the results
    of the assignment algorithm. It supports different result formats and
    uses the appropriate formatter based on the type of result.
    """

    def __init__(self) -> None:
        """
        Initializes an `OutputFormatter` object.
        """
        pass

    def _create_formatter(
        self, result_type: str 
    ) -> Union[FlowOutputFormatter, LPOutputFormatter]:
        FORMATTERS = {'flow': FlowOutputFormatter(), 'linear': LPOutputFormatter()}
        try:
            return FORMATTERS.get(result_type)
        except:
            raise ResultFormatNotFound('Formatter type not found')

    def format_result(
        self,
        result_context
    ) -> AssignmentResult:
        """
        Formats the algorithm result into a standardized structure.

        This method automatically detects the type of the result
        (either flow or simplex) and calls the corresponding formatter
        class to process it.

        Args:
            - result_context: The context of the result where each Formatter knows how to manage

        Returns:
            AssignmentResult: The formatted result, as processed by the appropriate
            formatter class.

        Raises:
            ResultFormatNotFound: If the result type is not recognized by
            any formatter.
        """
        try:
            result_type = result_context.get('type')
            formatter = self._create_formatter(result_type)
            return formatter.get_result(result_context)
        except:
            raise ResultFormatNotFound('Type of formatter not found')
