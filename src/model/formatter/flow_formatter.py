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

    def get_groups_topics(self, result: dict):
        """Returns a dictionary with groups as keys and assigned topic as values."""
        groups = {}
        for key, value in result.items():
            if self.__is_group_or_topic(key, GROUP_ID):
                for topic, topic_value in value.items():
                    if self.__topic_is_assigned(topic_value):
                        groups[key] = topic
        return groups

    def __tutor_is_assigned(self, value: bool):
        """Returns if the tutor was assigned to the topic."""
        return value > 0

    def get_topics_tutors(self, result: dict):
        """Returns a dictionary with topics as keys and assigned tutor as values."""
        topics = {}
        for key, value in result.items():
            if self.__is_group_or_topic(key, TOPIC_ID):
                for tutor, tutor_value in value.items():
                    if self.__tutor_is_assigned(tutor_value):
                        topics[key] = tutor
        return topics

    def __get_tutors(self, topics: dict, groups: dict):
        """Returns a dictionary with tutors as keys and assigned groups as values."""
        tutors = {}
        for topic, tutor in topics.items():
            assigned_groups = []
            for group, value in groups.items():
                if value == topic:
                    assigned_groups.append(group)
            tutors[tutor] = assigned_groups
        return tutors

    def get_tutors_groups(self, result: dict):
        """Returns algorithm results."""
        groups = self.get_groups_topics(result)
        topics = self.get_topics_tutors(result)
        tutors = self.__get_tutors(topics, groups)
        return tutors
