from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    topic = relationship("Topic", back_populates="topic_category", lazy="joined")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    category = Column(String, ForeignKey("categories.name"), nullable=False)

    topic_category = relationship("Category", back_populates="topic")
