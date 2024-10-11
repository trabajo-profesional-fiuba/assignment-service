from src.api.tutors.mapper import TutorMapper
from src.core.group import Group, UnassignedGroup


class GroupMapper:

    def __init__(
        self,
        tutor_mapper: TutorMapper | None = None,
    ) -> None:
        self._tutor_mapper = tutor_mapper

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
        tutor = None
        if self._tutor_mapper:
            tutor = self._tutor_mapper.convert_from_period_to_single_period_tutor(
                db_group.tutor_period
            )
        students_emails = [student.email for student in db_group.students]
        group = Group(
            id=db_group.id,
            tutor=tutor,
            students_emails=students_emails,
            reviewer_id=db_group.reviewer_id,
        )

        return group
