from src.api.dates.mapper import DateSlotsMapper
from src.api.topics.mapper import TopicMapper
from src.api.tutors.mapper import TutorMapper
from src.core.group import AssignedGroup, UnassignedGroup
from src.core.student import StudentMapper


class GroupMapper:
    @staticmethod
    def map_models_to_unassigned_groups(db_groups, topics):
        """Convierte desde una lista de grupos desde la bd a una lista de grupos sin asignar"""
        topics_mapped = {topic.id: topic for topic in topics}

        groups = [
            UnassignedGroup(
                id=db_group.id,
                students=[student.id for student in db_group.students],
                topics=[
                    topics_mapped[topic_id] for topic_id in db_group.preferred_topics
                ],
                group_number=db_group.group_number,
            )
            for db_group in db_groups
        ]

        return groups

    @staticmethod
    def map_model_to_assigned_group(db_group):
        """Convierte desde un de grupos desde la bd a un grupos asignados"""
        tutor = TutorMapper.map_tutor_period_to_tutor(db_group.tutor_period)
        students = StudentMapper.map_models_to_students(db_group.students)
        topic = TopicMapper.map_model_to_topic(db_group.topic)
        group = AssignedGroup(
            id=db_group.id,
            tutor=tutor,
            students=students,
            reviewer_id=db_group.reviewer_id,
            topic_assigned=topic,
            available_dates=DateSlotsMapper.map_models_to_date_slots(
                db_group.group_dates_slots
            ),
            group_number=db_group.group_number,
            assigned_date=DateSlotsMapper.map_datetime_to_date_slot(
                db_group.exhibition_date
            ),
        )

        return group

    @staticmethod
    def map_models_to_assigned_groups(db_groups):
        """Convierte desde una lista de grupos desde la bd a una lista de grupos asignados"""
        groups = list()
        for group in db_groups:
            groups.append(GroupMapper.map_model_to_assigned_group(group))

        return groups
