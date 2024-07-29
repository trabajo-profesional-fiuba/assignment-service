from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from src.api.users.model import User
from src.api.tutors.schemas import PeriodResponse, PeriodRequest
from src.api.tutors.model import Period,TutorPeriod
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_period(self, period: PeriodRequest):
        with self.Session() as session:
            period_obj = Period(id=period.id)
            session.add(period_obj)
            session.commit()
            session.refresh(period_obj)
            return PeriodResponse.model_validate(period_obj)

    def get_all_periods(self, order: str):
        with self.Session() as session:
            if order == "ASC":
                order_clause = asc(Period.created_at)
            elif order == "DESC":
                order_clause = desc(Period.created_at)
            else:
                raise ValueError("Invalid order direction. Use 'ASC' or 'DESC'.")

            results = session.query(Period).order_by(order_clause).all()
            return results


    def get_all_periods_by_id(self,tutor_id, order: str):
        with self.Session() as session:
            if order == "ASC":
                order_clause = asc(Period.created_at)
            elif order == "DESC":
                order_clause = desc(Period.created_at)
            else:
                raise ValueError("Invalid order direction. Use 'ASC' or 'DESC'.")

            results = session.query(TutorPeriod).join(User).filter(User.id == tutor_id).order_by(order_clause).all()
            return results