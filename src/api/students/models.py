from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


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
