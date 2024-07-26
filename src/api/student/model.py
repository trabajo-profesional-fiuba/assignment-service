from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.config.database import Base


class Student(Base):
    __tablename__ = "students"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    # Set relationship with GroupFormPreferences
    group_preferences = relationship(
        "GroupFormPreferences", back_populates="student", uselist=True, lazy="select")
