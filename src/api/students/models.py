from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class StudentPeriod(Base):
    __tablename__ = "student_periods"

    period_id = Column(String, ForeignKey("periods.id", ondelete="CASCADE"))
    student_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    __table_args__ = (
        UniqueConstraint("student_id", "period_id", name="uq_student_period"),
    )

    period = relationship(
        "Period", back_populates="student_periods", lazy="noload", cascade="all, delete"
    )
    student = relationship(
        "User", back_populates="student_periods", lazy="noload", cascade="all, delete"
    )
