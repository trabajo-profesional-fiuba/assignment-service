from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, inspect
from sqlalchemy.orm import relationship
from src.api.users.model import User, Role
from src.config.database.base import Base
from sqlalchemy.orm import validates
from src.api.form.exceptions import StudentNotFound


class FormPreferences(Base):
    __tablename__ = "form_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(DateTime, nullable=False)
    topic_1 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_2 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_3 = Column(String, ForeignKey("topics.name"), nullable=False)

    # Set relationship with Student
    student = relationship("User", back_populates="form_preferences")
