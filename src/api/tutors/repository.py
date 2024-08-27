from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, exc

from src.api.users.models import User, Role
from src.api.tutors.models import Period, TutorPeriod
from src.api.tutors.exceptions import (
    TutorNotFound,
    PeriodDuplicated,
    TutorPeriodNotFound,
)
from src.api.topics.models import Topic, TopicTutorPeriod
from src.api.topics.exceptions import TopicNotFound


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def _order_clause(self, order):
        if order == "ASC":
            return asc(Period.created_at)
        elif order == "DESC":
            return desc(Period.created_at)
        else:
            raise ValueError("Invalid order direction. Use 'ASC' or 'DESC'.")

    def add_period(self, period: Period) -> Period:
        try:
            with self.Session() as session:
                session.add(period)
                session.commit()
                session.refresh(period)
                session.expunge(period)

            return period
        except exc.IntegrityError:
            raise PeriodDuplicated(message="Period already exist")

    def is_tutor(self, tutor_id) -> bool:
        with self.Session() as session:
            exists = (
                session.query(User)
                .filter(User.role == Role.TUTOR)
                .filter(User.id == tutor_id)
                .first()
            )
            return True if exists else False

    def add_tutor_period(self, tutor_id, period_id) -> TutorPeriod:
        try:
            with self.Session() as session:
                period_obj = TutorPeriod(period_id=period_id, tutor_id=tutor_id)
                session.add(period_obj)
                session.commit()
                session.refresh(period_obj)
                tutor = session.get(User, tutor_id)
                session.expunge(tutor)

            return tutor
        except exc.IntegrityError:
            raise PeriodDuplicated(message="Period can't be assigned to tutor")
    
    def add_tutor_periods(self, tutor_periods: list[TutorPeriod]):
        try:
            with self.Session() as session:
                session.add_all(tutor_periods)
                session.commit()
                session.expunge_all()

            return tutor_periods
        except exc.IntegrityError as e:
            raise PeriodDuplicated(message=f"{e}")


    def get_all_periods(self, order: str) -> list[Period]:
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = session.query(Period).order_by(order_clause).all()
            session.expunge_all()
        return results

    def get_tutor_by_tutor_id(self, tutor_id) -> User:
        with self.Session() as session:
            tutor = session.query(User).filter(User.id == tutor_id).first()
            if tutor is None:
                raise TutorNotFound("Tutor doesn't exists")
            session.expunge(tutor)

        return tutor

    def get_tutor_period_by_tutor_email(self, period, tutor_email) -> TutorPeriod:
        with self.Session() as session:
            tutor_period = (
                session.query(TutorPeriod)
                .join(User)
                .filter(User.email == tutor_email)
                .filter(TutorPeriod.period_id == period)
            ).first()

            if tutor_period is None:
                raise TutorNotFound(
                    "The tutor does not exits or this period is not present"
                )

            session.expunge(tutor_period)

        return tutor_period

    def add_topic_tutor_period(
        self, tutor_email: str, topics: list[Topic], capacities: list[int]
    ):
        with self.Session() as session:
            topic_tutor_periods = []
            tutor = session.query(User).filter(User.email == tutor_email).first()
            if tutor:
                tutor_period = (
                    session.query(TutorPeriod)
                    .filter(TutorPeriod.tutor_id == tutor.id)
                    .first()
                )
                if tutor_period:
                    for idx, topic in enumerate(topics):
                        topic = (
                            session.query(Topic)
                            .filter(
                                Topic.name == topic.name
                                and Topic.category == topic.category
                            )
                            .first()
                        )
                        topic_tutor_period = TopicTutorPeriod(
                            topic_id=topic.id,
                            tutor_period_id=tutor_period.id,
                            capacity=capacities[idx],
                        )
                        session.add(topic_tutor_period)
                        topic_tutor_periods.append(topic_tutor_period)

                    session.commit()

                    for topic_tutor_period in topic_tutor_periods:
                        session.refresh(topic_tutor_period)
                        session.expunge(topic_tutor_period)

                    return topic_tutor_periods
                raise TutorPeriodNotFound(f"Tutor '{tutor_email}' has no period.")
            raise TutorNotFound(f"Tutor '{tutor_email}' not found.")

    def get_tutors(self):
        with self.Session() as session:
            tutors = session.query(User).filter(User.role == Role.TUTOR).all()
            session.expunge_all()
        return tutors

    def get_topic_tutor_period(
        self, topic_id: int, tutor_period_id: int
    ) -> TutorPeriod:
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.id == topic_id).first()
            if topic:
                tutor_period = (
                    session.query(TutorPeriod)
                    .filter(TutorPeriod.id == tutor_period_id)
                    .first()
                )
                if tutor_period:
                    return (
                        session.query(TopicTutorPeriod)
                        .filter(
                            TopicTutorPeriod.topic_id == topic_id
                            and TopicTutorPeriod.tutor_period_id == tutor_period_id
                        )
                        .first()
                    )
                else:
                    raise TutorPeriodNotFound("Tutor period not found.")
            else:
                raise TopicNotFound("Topic not found.")

    def delete_tutor_by_id(self, tutor_id):
        with self.Session() as session:
            tutor = (
                session.query(User)
                .filter(User.role == Role.TUTOR and User.id == tutor_id)
                .first()
            )
            if not tutor:
                raise TutorNotFound(f"Tutor with id: {tutor_id} not exists")

            session.delete(tutor)
            session.commit()

        return tutor

    def delete_tutors_periods_by_period_id(self, period_id):
        with self.Session() as session:
            session.query(TutorPeriod).filter(TutorPeriod.period_id == period_id).delete()
            session.commit()

    def get_tutors_by_period_id(self, period_id):
        with self.Session() as session:
            tutors = (
                session.query(User)
                .join(TutorPeriod)
                .filter(TutorPeriod.period_id == period_id)
                .all()
            )
            session.expunge_all()

        for tutor in tutors:
            tutor.periods = [period for period in tutor.periods if period.period_id == period_id]

        return tutors
