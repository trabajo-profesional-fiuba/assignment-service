from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy import exc

from src.api.users.model import User,Role

from src.api.tutors.schemas import PeriodResponse, PeriodRequest, TutorResponse
from src.api.tutors.model import Period, TutorPeriod
from src.api.tutors.exceptions import TutorNotFound, PeriodDuplicated


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
        try:
            with self.Session() as session:
                period_obj = Period(id=period.id)
                session.add(period_obj)
                session.commit()
                session.refresh(period_obj)
                return PeriodResponse.model_validate(period_obj)
        except exc.IntegrityError as e:
            raise PeriodDuplicated(message="Period already exist")
    
    def is_tutor(self, tutor_id):
        with self.Session() as session:
            exists = session.query(User).filter(User.rol == Role.TUTOR).filter(User.id == tutor_id).first()
            return (True if exists else False)

    def add_tutor_period(self, tutor_id, period_id):
        try:
            with self.Session() as session:
                period_obj = TutorPeriod(period_id=period_id, tutor_id=tutor_id)
                session.add(period_obj)
                session.commit()
                tutor = period_obj.tutor
                tutor_response = TutorResponse.model_validate(tutor)
                return tutor_response
        except exc.IntegrityError as e:
            raise PeriodDuplicated(message="Period can't be assigned to tutor")

    def get_all_periods(self, order: str):
        with self.Session() as session:
            order_clause = self._order_clause(order)
            results = session.query(Period).order_by(order_clause).all()
            return results

    def get_all_periods_by_id(self, tutor_id):
        with self.Session() as session:
            tutor = session.query(User).filter(User.id == tutor_id).first()
            if tutor:
                tutor_response = TutorResponse.model_validate(tutor)
                return tutor_response
            else:
                raise TutorNotFound("Tutor doesn't exists")