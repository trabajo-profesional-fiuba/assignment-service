from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class FormPreferences(Base):
    __tablename__ = "form_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(DateTime, nullable=False)
    topic_1 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_2 = Column(String, ForeignKey("topics.name"), nullable=False)
    topic_3 = Column(String, ForeignKey("topics.name"), nullable=False)

    student = relationship("User", lazy="noload")
