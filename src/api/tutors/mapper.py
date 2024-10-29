from src.api.dates.maper import DateSlotsMapper
from src.api.topics.mapper import TopicMapper
from src.api.tutors.models import TutorPeriod
from src.api.users.models import User
from src.core.topic import Topic
from src.core.tutor import Tutor


class TutorMapper:

    def __init__(
        self,
    ) -> None:
        self._topic_mapper = TopicMapper()

    def map_tutor_period_to_tutors(self, db_periods: list[TutorPeriod]):
        """A partir de cuatrimestres de tutores, crean un tutor"""
        tutors = list()
        for db_period in db_periods:
            db_tutor = db_period.tutor
            topics = self._topic_mapper.map_models_to_topics(db_period.topics)
            tutor = Tutor(
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

    def map_tutor_period_to_tutor(
        self, db_tutor_period: TutorPeriod, topics: list[Topic] = []
    ):
        """A partir de un cuatrimestre, crean un tutor"""
        tutor = None
        if db_tutor_period:
            tutor = Tutor(
                id=db_tutor_period.tutor_id,
                period_id=db_tutor_period.id,
                name=db_tutor_period.tutor.name,
                last_name=db_tutor_period.tutor.last_name,
                email=db_tutor_period.tutor.email,
                capacity=db_tutor_period.capacity,
                topics=topics,
            )
        return tutor

    def map_models_to_tutors(self, db_tutors: list[User]):
        """A partir de una lista de usuarios desde la bd crea una lista de tutores"""
        tutors = list()
        for user in db_tutors:
            period = user.tutor_periods[0]
            topics = self._topic_mapper.map_models_to_topics(period.topics)
            dates = DateSlotsMapper.map_models_to_date_slots(user.tutor_dates_slots)
            tutor = Tutor(
                id=user.id,
                period_id=period.id,
                name=user.name,
                last_name=user.last_name,
                email=user.email,
                topics=topics,
                capacity=period.capacity,
                is_evaluator=period.is_evaluator,
                available_dates=dates,
            )
            tutors.append(tutor)

        return tutors
