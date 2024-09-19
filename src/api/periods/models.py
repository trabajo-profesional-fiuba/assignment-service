from sqlalchemy import Column, String, Boolean, DateTime
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

    tutor_periods = relationship("TutorPeriod", back_populates="period", lazy="noload")
    groups = relationship("Group", back_populates="period", lazy="noload")
    student_periods = relationship(
        "StudentPeriod", back_populates="period", lazy="noload"
    )
