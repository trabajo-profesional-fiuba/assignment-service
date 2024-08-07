from src.config.database.base import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    DateTime,
    UniqueConstraint,
)
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

    id = Column(Integer, autoincrement=True, primary_key=True)
    period_id = Column(String, ForeignKey("periods.id"))
    tutor_id = Column(Integer, ForeignKey("users.id"), index=True)
    capacity = Column(Integer, default=0)
    is_evaluator = Column(Boolean, default=False)

    tutor = relationship("User", back_populates="periods",lazy="joined")
    period = relationship("Period", back_populates="periods")
    groups = relationship(
        "Group", back_populates="tutor_period", uselist=True, lazy="noload"
    )

    __table_args__ = (
        UniqueConstraint("period_id", "tutor_id", name="tutor_period_const"),
    )
