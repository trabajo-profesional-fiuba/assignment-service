from sqlalchemy.orm import Session
from sqlalchemy import insert

from src.api.dates.models import DateSlot, GroupDateSlot, TutorDateSlot


class DateSlotRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_date_slot(self, date_slot: DateSlot):

        with self.Session() as session:
            session.add(date_slot)
            session.commit()
            session.refresh(date_slot)

            session.expunge(date_slot)

        return date_slot

    def add_bulk(
        self, model: DateSlot | GroupDateSlot | TutorDateSlot, data: list[dict]
    ):
        with self.Session() as session:
            result = session.execute(insert(model).returning(model), data)
            session.commit()

            # Extract the inserted rows from the result
            rows = result.fetchall()
            session.expunge_all()
            saved_data = [getattr(row, model.__name__) for row in rows]

        return saved_data

    def get_slots_by_period(self, period: str):
        with self.Session() as session:
            slots = session.query(DateSlot).filter(DateSlot.period_id == period).all()
            for slot in slots:
                session.expunge(slot)

        return slots
