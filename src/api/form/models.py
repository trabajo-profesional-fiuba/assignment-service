from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, inspect
from sqlalchemy.orm import relationship
from src.api.users.model import User, Role
from src.config.database import Base
from sqlalchemy.orm import validates
from src.api.form.exceptions import StudentNotFound


class GroupFormPreferences(Base):
    __tablename__ = "group_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.id"))
    group_id = Column(DateTime, nullable=False)
    topic_1 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_2 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_3 = Column(String, ForeignKey("topics.name"), nullable=False)

    # Set relationship with Student
    student = relationship("User", back_populates="group_preferences")
