from src.core.group import UnassignedGroup
from src.core.tutor import Tutor


class GroupMapper:

    def convert_from_models_to_unassigned_groups(self, db_groups, topics):
        topics_mapped = {topic.id: topic for topic in topics}

        groups = [
            UnassignedGroup(
                id=db_group.id,
                students=[student.id for student in db_group.students],
                topics=[
                    topics_mapped[topic_id] for topic_id in db_group.preferred_topics
                ],
            )
            for db_group in db_groups
        ]

        return groups

    def convert_from_model_to_group(self, db_group):
        tutor = Tutor()