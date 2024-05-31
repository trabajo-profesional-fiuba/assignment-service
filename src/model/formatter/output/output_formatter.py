from typing import Union, List, Tuple
from src.model.formatter.output.flow_formatter import FlowOutputFormatter
from src.model.formatter.output.simplex_formatter import SimplexOutputFormatter
from src.exceptions import ResultFormatNotFound


class OutputFormatter:
    """
    Class for formatting assignment algorithm results.

    This class provides a standardized interface for formatting the results
    of the assignment algorithm. It supports different result formats and
    uses the appropriate formatter based on the type of result.
    """

    FORMATTERS = {dict: FlowOutputFormatter(), list: SimplexOutputFormatter()}

    def __init__(self) -> None:
        """
        Initializes an `OutputFormatter` object.
        """
        pass

    def format_result(self, result: Union[dict, list]) -> List[Tuple[str, str, str]]:
        """
        Formats the algorithm result into a standardized structure.

        This method automatically detects the type of the result
        (either flow or simplex) and calls the corresponding formatter
        class to process it.

        Args:
            result (Union[dict, list]): The result of the assignment algorithm,
            which can be of type `dict` or `list`.

        Returns:
            Any: The formatted result, as processed by the appropriate
            formatter class.

        Raises:
            ResultFormatNotFound: If the result type is not recognized by
            any formatter.
        """
        result_type = type(result)
        formatter = self.FORMATTERS.get(result_type)
        if formatter:
            return formatter.get_result(result)
        else:
            raise ResultFormatNotFound("Unrecognized result format")
