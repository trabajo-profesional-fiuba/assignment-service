from src.config.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.api.users.model import User


class Period(Base):
    __tablename__ = "periods"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime(), server_default=func.now())

    periods = relationship("TutorPeriod", back_populates="period")


class TutorPeriod(Base):

    __tablename__ = "tutor_periods"

    id = Column(String, ForeignKey("periods.id"), primary_key=True)
    tutor_id = Column(Integer, ForeignKey("users.id"), index=True)
    capacity = Column(Integer, default=0)
    is_evaluator = Column(Boolean, default=False)

    tutor = relationship("User", back_populates="periods")
    period = relationship("Period", back_populates="periods")
