
import src.assignments.adapters.result_context as result_context
from src.assignments.adapters.exceptions import ResultFormatNotFound
from src.model.utils.result import AssignmentResult
from src.assignments.adapters.flow_adapter import FlowAdapter
from src.assignments.adapters.lp_adapter import LPAdapter




class ResultAdapter:
    """
    Class for adapting assignment algorithm results.

    This class provides a standardized interface for adapting the results
    of the assignment algorithm. It supports different result formats and
    uses the appropriate adapter based on the type of result.
    """

    def _build_adapter(
        self, result_type: str
    ):
        ADAPTERS = {"flow": FlowAdapter(), "linear": LPAdapter()}
        try:
            return ADAPTERS.get(result_type)
        except:
            raise ResultFormatNotFound("Adapter type not found")
 
    def adapt_results(self, result_context: 'result_context.ResultContext') -> AssignmentResult:
        """
        Adapts the algorithm result into a standardized structure.

        This method detects the type of the result
        (either flow or simplex) and calls the corresponding adapter
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
            result_type = result_context.get("type")
            adapter = self._build_adapter(result_type)
            return adapter.adapt_results(result_context)
        except:
            raise ResultFormatNotFound("Type of adapter not found")
