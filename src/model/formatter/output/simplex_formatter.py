from src.model.result import AssignmentResult


class SimplexOutputFormatter:
    """
    Formats the output of a simplex algorithm into a standardized structure.

    This formatter processes a list of strings representing assignments and splits
    each string to extract the group, tutor, and topic, creating a list of tuples
    representing the assignments in the format (group, topic, tutor).
    """

    def __init__(self) -> None:
        """
        Initializes a `SimplexOutputFormatter` object.
        """
        pass

    def get_result(self, result: list[str], groups) -> AssignmentResult:
        """
        Formats the simplex algorithm result into a standardized structure.

        Processes the result list and splits each assignment string to extract
        the group, tutor, and topic, and adds them to the standardized result
        as tuples (group, topic, tutor).

        Args:
            result (list[str]): The list of strings representing assignments.

        Returns:
            list[Tuple[str, str, str]]: A list of tuples representing the assignments
            in the format (group, topic, tutor).
        """
        assignments = []
        for assignment in result:
            parts = assignment.split("_")
            group = parts[1]
            topic = parts[2]
            tutor = parts[3]
            assignments.append((group, topic, tutor))
        return assignments
