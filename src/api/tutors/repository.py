from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from pydantic import TypeAdapter

from src.api.users.model import User
from src.api.users.schemas import UserResponse
from src.api.tutors.schemas import PeriodResponse, PeriodRequest, TutorPeriodResponse, TutorResponse
from src.api.tutors.model import Period, TutorPeriod
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted



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

    def add_period(self, period: PeriodRequest):
        with self.Session() as session:
            period_obj = Period(id=period.id)
            session.add(period_obj)
            session.commit()
            session.refresh(period_obj)
            return PeriodResponse.model_validate(period_obj)

    def add_tutor_period(self, tutor_id, period_id):
        with self.Session() as session:
            period_obj = TutorPeriod(id=period_id, tutor_id=tutor_id)
            session.add(period_obj)
            session.commit()
            tutor = period_obj.tutor
            tutor_response = TutorResponse.model_validate(tutor)
            return tutor_response

    def get_all_periods(self, order: str):
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = session.query(Period).order_by(order_clause).all()
            return results

    def get_all_periods_by_id(self, tutor_id, order: str):
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = (
                session.query(TutorPeriod)
                .join(User)
                .filter(User.id == tutor_id)
                .order_by(order_clause)
                .all()
            )
            return results
