from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    uid = Column(Integer, primary_key=True)
    group_id = Column(DateTime)
    topic_1 = Column(String, nullable=False)
    topic_2 = Column(String, nullable=False)
    topic_3 = Column(String, nullable=False)


class TopicCategory(Base):
    __tablename__ = "topic_category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(Integer, ForeignKey("topic_category.id"), nullable=False)

    topic_category = relationship("TopicCategory")
