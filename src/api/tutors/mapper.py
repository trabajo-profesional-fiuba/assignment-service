from typing import Optional
from src.api.topics.mapper import TopicMapper
from src.api.tutors.models import TutorPeriod

from src.core.topic import Topic
from src.core.tutor import SinglePeriodTutor


class TutorMapper:

    def __init__(self, topic_mapper: Optional[TopicMapper] = None) -> None:
        self._topic_mapper = topic_mapper

    def convert_to_single_period_tutors(self, db_periods: list[TutorPeriod]):
        tutors = list()
        for db_period in db_periods:
            db_tutor = db_period.tutor
            topics = self._topic_mapper.map_models_to_topics(db_period.topics) if self._topic_mapper else []
            tutor = SinglePeriodTutor(
                id=db_tutor.id,
                period_id=db_period.id,
                name=db_tutor.name,
                last_name=db_tutor.last_name,
                email=db_tutor.email,
                topics=topics,
                capacity=db_period.capacity,
            )
            tutors.append(tutor)

        return tutors

    def map_model_to_single_period_tutor(
        self, db_tutor_period: TutorPeriod, topics: list[Topic] = []
    ):
        tutor = SinglePeriodTutor(
            id=db_tutor_period.tutor_id,
            period_id=db_tutor_period.id,
            name=db_tutor_period.tutor.name,
            last_name=db_tutor_period.tutor.last_name,
            email=db_tutor_period.tutor.email,
            capacity=db_tutor_period.capacity,
            topics=topics,
        )
        return tutor
