from sqlalchemy import Column, String, DateTime
from storage.database import Base


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True, index=True)
    group_id = Column(DateTime)
    topic1 = Column(String)
    topic2 = Column(String)
    topic3 = Column(String)
