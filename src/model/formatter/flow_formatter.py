from src.constants import GROUP_ID, TOPIC_ID


class FlowResultFormatter:
    def __init__(self):
        pass

    def __is_group_or_topic(self, string: str, identifier: str):
        """Returns if the string represents a group or a topic."""
        return string.startswith(identifier)

    def __topic_is_assigned(self, value: bool):
        """Returns if the topic was assigned to the group."""
        return value == 1

    def __get_groups_topics(self, result: dict):
        """Returns a dictionary with groups as keys and assigned topic as values."""
        groups = {}
        for key, value in result.items():
            if self.__is_group_or_topic(key, GROUP_ID):
                for topic, assigned in value.items():
                    if self.__topic_is_assigned(assigned):
                        groups[key] = topic
        return groups

    def __tutor_is_assigned(self, value: bool):
        """Returns if the tutor was assigned to the topic."""
        return value > 0

    def __get_topics_tutors(self, result: dict):
        """Returns a dictionary with topics as keys and assigned tutor as values."""
        topics = {}
        for key, value in result.items():
            if self.__is_group_or_topic(key, TOPIC_ID):
                for tutor, tutor_value in value.items():
                    if self.__tutor_is_assigned(tutor_value):
                        topics[key] = tutor
        return topics

    def get_result(self, result):
        """
        Formats the flow algorithm result into a standardized structure.

        Processes the result dictionary and extracts assignments where the value is 1,
        and adds them to the standardized result as tuples (group, topic, tutor).
        """
        groups_topics = self.__get_groups_topics(result)
        topics_tutors = self.__get_topics_tutors(result)
        assignments = []

        for group, topic in groups_topics.items():
            if topic in topics_tutors:
                tutor = topics_tutors[topic]
                assignments.append((group, topic, tutor))
        return assignments
