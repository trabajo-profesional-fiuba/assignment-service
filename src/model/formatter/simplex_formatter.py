import re


class SimplexResultFormatter:
    def __init__(self):
        pass

    def __get_assigned_groups_by_tutors(self, data: dict):
        """
        Get a list of groups associated with each tutor from a given dictionary.

        Args:
            data (dict): A dictionary where keys are groups and values are dictionaries
            representing the association between topics and tutors for each group.

        Returns:
            dict: A dictionary where keys are topics and values are lists of groups
            associated with each topic.

        Example:
            >>> data = {
            ...     1: {"t1": "p2"},
            ...     2: {"t2": "p1"},
            ...     3: {"t3": "p4"}
            ... }
            >>> get_groups_by_tutor(data)
            {'p1': [2], 'p2': [1], 'p4': [3]}
        """
        topic_groups = {}
        for group, topics_tutors in data.items():
            for topic, tutor in topics_tutors.items():
                if tutor not in topic_groups:
                    topic_groups[tutor] = []
                topic_groups[tutor].append(group)
        return topic_groups

    def __get_assigned_topics_by_groups(self, data: dict):
        """
        Get a dictionary with groups as keys and assigned topics as values.

        Args:
            data (dict): A dictionary where keys are groups and values are dictionaries
            representing the association between topics and tutors for each group.

        Returns:
            dict: A dictionary where keys are groups and values are lists of
            assigned topics for each group.

        Example:
            >>> data = {
            ...     1: {"t1": "p2"},
            ...     2: {"t2": "p1"},
            ...     3: {"t3": "p4"}
            ... }
            >>> get_groups_assigned_topics(data)
            {1: ['t1'], 2: ['t2'], 3: ['t3']}
        """
        groups_assigned_topics = {}
        for group, topics_tutors in data.items():
            assigned_topics = []
            for topic, tutor in topics_tutors.items():
                assigned_topics.append(topic)
            groups_assigned_topics[group] = assigned_topics
        return groups_assigned_topics

    def __get_results(self, result: dict):
        """
        Returns algorithm results.

        Args:
            - result: List of selected variables.

        Returns a dictionary that represents the assignment results.
        """
        original_dict = {}
        pattern = re.compile(r"Assignment_(\d+)_(\w+)_(\w+)")
        for var_name in result:
            match = pattern.match(var_name)
            if match:
                i, topic, tutor = match.groups()
                i = int(i)
                if i not in original_dict:
                    original_dict[i] = {}
                original_dict[i][topic] = tutor

        return original_dict

    def get_tutors_groups(self, result: dict):
        data = self.__get_results(result)
        groups_tutors = self.__get_assigned_groups_by_tutors(data)
        return groups_tutors

    def get_groups_topics(self, result: dict):
        data = self.__get_results(result)
        topics_groups = self.__get_assigned_topics_by_groups(data)
        return topics_groups
