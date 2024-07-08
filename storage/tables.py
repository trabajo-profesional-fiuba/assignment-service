from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


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
    Index('idx_name_category', name, category)

class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True)
    group_id = Column(DateTime)
    topic_1 = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic_2 = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic_3 = Column(Integer, ForeignKey("topic.id"), nullable=False)

    topic_1_rel = relationship(
        "Topic",
        primaryjoin="TopicPreferences.topic_1 == Topic.id",
        foreign_keys=[topic_1],
    )
    topic_2_rel = relationship(
        "Topic",
        primaryjoin="TopicPreferences.topic_2 == Topic.id",
        foreign_keys=[topic_2],
    )
    topic_3_rel = relationship(
        "Topic",
        primaryjoin="TopicPreferences.topic_3 == Topic.id",
        foreign_keys=[topic_3],
    )
