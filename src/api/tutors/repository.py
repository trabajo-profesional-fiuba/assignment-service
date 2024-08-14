from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, exc

from src.api.users.model import User, Role
from src.api.tutors.model import Period, TutorPeriod
from src.api.tutors.exceptions import (
    TutorNotFound,
    PeriodDuplicated,
    TutorPeriodNotFound,
)
from src.api.topic.models import Topic, TopicTutorPeriod


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

    def get_all_periods(self, order: str) -> list[Period]:
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = session.query(Period).order_by(order_clause).all()
            session.expunge_all()
        return results

    def get_all_periods_by_id(self, tutor_id) -> User:
        with self.Session() as session:
            tutor = session.query(User).filter(User.id == tutor_id).first()
            if tutor is None:
                raise TutorNotFound("Tutor doesn't exists")

            session.expunge(tutor)

        return tutor

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
                        session.expunge(topic_tutor_period)
                        topic_tutor_periods.append(topic_tutor_period)
                    session.commit()
                    return topic_tutor_periods
                raise TutorPeriodNotFound(f"Tutor '{tutor_email}' has no period.")
            raise TutorNotFound(f"Tutor '{tutor_email}' not found.")

    def get_tutor_period_by_email(self, period, tutor_email) -> TutorPeriod:
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
