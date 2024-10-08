from datetime import datetime
from sqlalchemy.orm import Session


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