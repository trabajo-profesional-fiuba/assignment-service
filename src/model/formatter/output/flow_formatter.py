from typing import Dict, Tuple
from src.constants import GROUP_ID, TOPIC_ID


class FlowOutputFormatter:
    """
    Formats the output of a flow algorithm into a standardized structure.

    This formatter processes the result dictionary from a flow algorithm and extracts
    assignments where the value is 1, creating a list of tuples representing the
    assignments in the format (group, topic, tutor).
    """

    def __init__(self) -> None:
        """
        Initializes a FlowOutputFormatter object.
        """
        pass

    def _is_group_or_topic(self, string: str, identifier: str) -> bool:
        """
        Checks if the string represents a group or a topic.

        Args:
            string (str): The string to check.
            identifier (str): The identifier for either a group or a topic.

        Returns:
            bool: True if the string represents a group or a topic, False otherwise.
        """
        return string.startswith(identifier)

    def _topic_is_assigned(self, is_assigned: bool) -> bool:
        """
        Checks if the topic was assigned to the group.

        Args:
            is_assigned (bool): The value indicating whether the topic is assigned.

        Returns:
            bool: True if the topic was assigned, False otherwise.
        """
        return is_assigned == 1

    def _get_groups_topics(self, result: Dict[str, Dict[str, int]]) -> Dict[str, str]:
        """
        Extracts groups and their assigned topics from the result.

        Args:
            result (Dict[str, Dict[str, int]]): The result dictionary from the flow
            algorithm.

        Returns:
            Dict[str, str]: A dictionary with groups as keys and assigned topics as
            values.
        """
        groups = {}
        for key, value in result.items():
            if self._is_group_or_topic(key, GROUP_ID):
                for topic, assigned in value.items():
                    if self._topic_is_assigned(assigned):
                        groups[key] = topic
        return groups

    def _tutor_is_assigned(self, is_assigned: int) -> bool:
        """
        Checks if the tutor was assigned to the topic.

        Args:
            is_assigned (int): The value indicating the assignment of the tutor.

        Returns:
            bool: True if the tutor was assigned, False otherwise.
        """
        return is_assigned > 0

    def _get_topics_tutors(self, result: Dict[str, Dict[str, int]]) -> Dict[str, str]:
        """
        Extracts topics and their assigned tutors from the result.

        Args:
            result (Dict[str, Dict[str, int]]): The result dictionary from the flow
            algorithm.

        Returns:
            Dict[str, str]: A dictionary with topics as keys and assigned tutors as
            values.
        """
        topics = {}
        for key, value in result.items():
            if self._is_group_or_topic(key, TOPIC_ID):
                for tutor, tutor_value in value.items():
                    if self._tutor_is_assigned(tutor_value):
                        topics[key] = tutor
        return topics

    def get_result(
        self, result: Dict[str, Dict[str, int]]
    ) -> list[Tuple[str, str, str]]:
        """
        Formats the flow algorithm result into a standardized structure.

        Processes the result dictionary and extracts assignments where the value is 1,
        and adds them to the standardized result as tuples (group, topic, tutor).

        Args:
            result (Dict[str, Dict[str, int]]): The result dictionary from the flow
            algorithm.

        Returns:
            list[Tuple[str, str, str]]: A list of tuples representing the assignments in
            the format (group, topic, tutor).
        """
        groups_topics = self._get_groups_topics(result)
        topics_tutors = self._get_topics_tutors(result)
        assignments = []

        for group, topic in groups_topics.items():
            if topic in topics_tutors:
                tutor = topics_tutors[topic]
                assignments.append((group, topic, tutor))
        return assignments
