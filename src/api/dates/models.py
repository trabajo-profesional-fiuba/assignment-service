from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class DateSlot(Base):
    __tablename__ = "dates_slots"

    period_id = Column(
        String, ForeignKey("periods.id", ondelete="CASCADE"), primary_key=True
    )
    slot = Column(DateTime(timezone=False), primary_key=True)

    # relationships
    period = relationship("Period", back_populates="dates_slots", lazy="noload")
