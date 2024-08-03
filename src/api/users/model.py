from sqlalchemy import Column, String, Integer, Enum
from src.config.database.base import Base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship


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
        "FormPreferences", back_populates="student", uselist=False, lazy="select"
    )
    # immediate - items should be loaded as the parents are loaded,
    #using a separate SELECT statement
    periods = relationship(
        "TutorPeriod", back_populates="tutor", uselist=True, lazy="immediate"
    )
