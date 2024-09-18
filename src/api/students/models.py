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
from src.config.database.base import Base
from src.api.periods.models import Period


class StudentPeriod(Base):
    __tablename__ = "student_periods"

    period_id = Column(
        String, ForeignKey("periods.id", ondelete="CASCADE"), primary_key=True
    )
    student_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    period = relationship(
        "Period", back_populates="student_periods", lazy="noload", cascade="all, delete"
    )
    student = relationship(
        "User", back_populates="student_periods", lazy="noload", cascade="all, delete"
    )
