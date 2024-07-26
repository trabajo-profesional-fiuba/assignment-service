from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.api.student.model import Student
from src.config.database import Base



class GroupFormPreferences(Base):
    __tablename__ = "group_preferences"

    uid = Column(Integer, ForeignKey("students.uid"), primary_key=True)
    group_id = Column(DateTime)
    topic_1 = Column(String, nullable=False)
    topic_2 = Column(String, nullable=False)
    topic_3 = Column(String, nullable=False)

    # Set relationship with Student
    student = relationship("Student", back_populates="group_preferences")
