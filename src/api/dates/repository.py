from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import insert, exc

from src.api.dates.models import DateSlot
from src.config.logging import logger


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

    def bulk_insert(self, date_slots: list[dict]):
        with self.Session() as session:
            result = session.execute(insert(DateSlot).returning(DateSlot), date_slots)
            session.commit()
            
            # Extract the inserted rows from the result
            rows = result.fetchall()
            session.expunge_all()
            date_slots_saved = [row.DateSlot for row in rows]
            
        return date_slots_saved
