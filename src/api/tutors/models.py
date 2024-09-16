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


class Period(Base):
    __tablename__ = "periods"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime(), server_default=func.now())
    form_active = Column(Boolean, default=True)
    initial_project_active = Column(Boolean, default=False)
    intermediate_project_active = Column(Boolean, default=False)
    final_project_active = Column(Boolean, default=False)

    tutor_periods = relationship("TutorPeriod", back_populates="period")
    groups = relationship("Group", back_populates="period")
    student_periods = relationship("StudentPeriod", back_populates="period")


class TutorPeriod(Base):

    __tablename__ = "tutor_periods"

    id = Column(Integer, autoincrement=True, primary_key=True)
    period_id = Column(String, ForeignKey("periods.id", ondelete="SET NULL"))
    tutor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    capacity = Column(Integer, default=0)
    is_evaluator = Column(Boolean, default=False)

    tutor = relationship("User", back_populates="tutor_periods", lazy="subquery")
    period = relationship("Period", back_populates="tutor_periods")
    topics = relationship("Topic", secondary="topics_tutor_periods", lazy="subquery")
    groups = relationship(
        "Group", back_populates="tutor_period", uselist=True, lazy="noload"
    )

    __table_args__ = (
        UniqueConstraint("period_id", "tutor_id", name="tutor_period_const"),
    )


class StudentPeriod(Base):
    __tablename__ = "student_periods"

    period_id = Column(String, ForeignKey("periods.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    period = relationship("Period", back_populates="student_periods", lazy="noload")
    student = relationship("User", back_populates="student_periods", lazy="noload")
