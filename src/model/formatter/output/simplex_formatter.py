class SimplexResultFormatter:
    def __init__(self):
        pass

    def get_result(self, result):
        """
        Formats the simplex algorithm result into a standardized structure.

        Processes the result list and splits each assignment string to extract group,
        tutor, and topic, and adds them to the standardized result as tuples
        (group, topic, tutor).
        """
        assignments = []
        for assignment in result:
            parts = assignment.split("_")
            group = parts[1]
            topic = parts[2]
            tutor = parts[3]
            assignments.append((group, topic, tutor))
        return assignments
