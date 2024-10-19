from src.api.topics.mapper import TopicMapper
from src.api.tutors.mapper import TutorMapper
from src.core.group import AssignedGroup, UnassignedGroup
from src.core.student import StudentMapper


class GroupMapper:

    def __init__(
        self,
    ) -> None:
        self._tutor_mapper = TutorMapper()
        self._student_mapper = StudentMapper()
        self._topic_mapper = TopicMapper()

    def map_models_to_unassigned_groups(self, db_groups, topics):
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

    def map_model_to_assigned_group(self, db_group):
        tutor = self._tutor_mapper.map_model_to_tutor(db_group.tutor_period)
        students = self._student_mapper.map_models_to_students(db_group.students)
        topic = self._topic_mapper.map_model_to_topic(db_group.topic)
        group = AssignedGroup(
            id=db_group.id,
            tutor=tutor,
            students=students,
            reviewer_id=db_group.reviewer_id,
            topic_assigned=topic,
        )

        return group
