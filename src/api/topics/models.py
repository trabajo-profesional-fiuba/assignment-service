from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    topic = relationship(
        "Topic",
        back_populates="category",
        lazy="joined",
        cascade="all, delete-orphan",
    )


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )

    category = relationship("Category", back_populates="topic", lazy="subquery")
    groups = relationship("Group", back_populates="topic", lazy="noload")


class TopicTutorPeriod(Base):
    __tablename__ = "topics_tutor_periods"

    topic_id = Column(ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True)
    tutor_period_id = Column(
        ForeignKey("tutor_periods.id", ondelete="CASCADE"), primary_key=True
    )
    capacity = Column(Integer, default=1)
