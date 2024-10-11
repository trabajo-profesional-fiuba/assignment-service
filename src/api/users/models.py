from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Enum
from src.config.database.base import Base


class Role(PyEnum):
    STUDENT = "student"
    TUTOR = "tutor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    role = Column(Enum(Role))

    form_preferences = relationship(
        "FormPreferences",
        back_populates="student",
        uselist=False,
        lazy="noload",
        cascade="all, delete",
    )
    # immediate - items should be loaded as the parents are loaded,
    # using a separate SELECT statement
    tutor_periods = relationship(
        "TutorPeriod",
        back_populates="tutor",
        uselist=True,
        lazy="noload",
        cascade="all, delete-orphan",
    )
    student_periods = relationship(
        "StudentPeriod",
        back_populates="student",
        lazy="noload",
        cascade="all, delete-orphan",
    )
    tutor_dates_slots = relationship(
        "TutorDateSlot", back_populates="tutors", lazy="noload"
    )
