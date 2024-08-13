from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    topic = relationship("Topic", back_populates="topic_category", lazy="joined")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    category = Column(String, ForeignKey("categories.name"), nullable=False)

    topic_category = relationship("Category", back_populates="topic")


class TopicTutorPeriod(Base):
    __tablename__ = "topics_tutor_periods"

    topic_id = Column(ForeignKey("topics.id"), primary_key=True)
    tutor_period_id = Column(ForeignKey("tutor_periods.id"), primary_key=True)
    capacity = Column(Integer, default=1)
