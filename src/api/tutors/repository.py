from sqlalchemy.orm import Session
from sqlalchemy import exc

from src.api.tutors.schemas import PeriodResponse, PeriodRequest
from src.api.tutors.model import Period
from src.api.tutors.exceptions import TutorDuplicated, TutorNotInserted


class TutorRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_period(self, period: PeriodRequest):
        with self.Session() as session:
            period_obj = Period(
                id=period.id
            )
            session.add(period_obj)
            session.commit()
            session.refresh(period_obj)
            return PeriodRequest.validate(period_obj)
