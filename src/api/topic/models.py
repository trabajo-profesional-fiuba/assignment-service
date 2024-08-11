from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.config.database.base import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("topic_id", ForeignKey("topics.id"), primary_key=True),
    Column("tutor_period_id", ForeignKey("tutor_periods.id"), primary_key=True),
)


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
