from sqlalchemy import Column, String, DateTime, Table
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True, index=True)
    group_id = Column(DateTime)
    topic_1 = Column(String)
    topic_2 = Column(String)
    topic_3 = Column(String)
