from src.core.group import BaseGroup


class GroupMapper:

    def convert_from_models_to_base_groups(self, db_groups, topics):
        topics_mapped = {}
        for topic in topics:
            topics_mapped[topic.id] = topic

        groups = list()
        for db_group in db_groups:
            id = db_group.id
            students = [student.id for student in db_group.students]
            group_topics = [topics_mapped[id] for id in db_group.preferred_topics]

            group = BaseGroup(id=id, students=students, topics=group_topics)
            groups.append(group)

        return groups
