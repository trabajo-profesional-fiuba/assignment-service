from src.assignments.adapters.exceptions import EvaluatorNotFound
from src.exceptions import WrongDateFormat
from src.model.utils.result import AssignmentResult
from src.model.utils.delivery_date import DeliveryDate
from src.constants import GROUP_ID,EVALUATOR_ID


class FlowAdapter:

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

    def _find_evaluator(self, evaluators: list, id: int):
        for evaluator in evaluators:
            if evaluator.id() == id:
                return evaluator

        return EvaluatorNotFound(
            f"Evaluator with id: {id} was not found in the current evaluator list"
        )

    def _adapt_groups_and_evaluators(self, groups, evaluators, g_info, e_info):
        results = []
        if g_info:
            for group in groups:
                group_key = f"{GROUP_ID}-{group.id()}"
                group_edges = g_info[group_key]
                evaluator_id = e_info[group_key][1]
                for key, value in group_edges.items():
                    if value == 1:
                        date = self._create_date(key)
                        evaluator = self._find_evaluator(evaluators, evaluator_id)

                        group.assign_date(date)
                        evaluator.evaluate_date(date)
                        results.append((group_key, f"{EVALUATOR_ID}-{evaluator_id}", key))

        return results

    def adapt_results(self, result_context) -> AssignmentResult:
        """
        Adapts the flow algorithm result into a standardized structure.

        Args:
            result_context

        Returns:
            AssignmentResult instance.
        """
        groups_information = result_context.get("groups_results")
        groups = result_context.get("groups")

        evaluators_information = result_context.get("evaluators_results")
        evaluators = result_context.get("evaluators")

        substitutes = result_context.get("substitutes")

        if groups is None or evaluators is None:
            return AssignmentResult([], substitutes)

        results = self._adapt_groups_and_evaluators(
            groups, evaluators, groups_information, evaluators_information
        )

        return AssignmentResult(results, substitutes)
