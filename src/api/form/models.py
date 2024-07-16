from sqlalchemy import Column, String, DateTime, Integer

from src.config.database import Base

class GroupFormSubmittion(Base):
    __tablename__ = "group_submitions"

    uid = Column(Integer, primary_key=True)
    group_id = Column(DateTime)
    topic_1 = Column(String, nullable=False)
    topic_2 = Column(String, nullable=False)
    topic_3 = Column(String, nullable=False)
