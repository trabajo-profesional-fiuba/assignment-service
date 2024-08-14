from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class FormPreferences(Base):
    """
    A FormPreference is a answer that is send by a student
    when the period started
    """
    __tablename__ = "form_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(DateTime, nullable=False)
    topic_1 = Column(Integer, ForeignKey("topics.id"), nullable=False)
    topic_2 = Column(Integer, ForeignKey("topics.id"), nullable=False)
    topic_3 = Column(Integer, ForeignKey("topics.id"), nullable=False)

    student = relationship("User", lazy="noload")
