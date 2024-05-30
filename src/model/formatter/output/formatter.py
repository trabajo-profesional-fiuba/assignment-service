from src.model.formatter.output.flow_formatter import FlowResultFormatter
from src.model.formatter.output.simplex_formatter import SimplexResultFormatter


class ResultFormatter:
    """Class for formatting assignment algorithm results."""

    FORMATTERS = {dict: FlowResultFormatter(), list: SimplexResultFormatter()}

    def __init__(self):
        """
        Initializes a ResultFormatter object.
        """
        pass

    def format_result(self, result):
        """
        Formats the algorithm result into a standardized structure.

        Automatically detects the type of result (flow or simplex) and calls the
        corresponding formatter class to process it.
        """
        result_type = type(result)
        formatter = self.FORMATTERS.get(result_type)
        if formatter:
            return formatter.get_result(result)
        else:
            raise ValueError("Unrecognized result format")
