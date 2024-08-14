from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database.base import Base


class FormPreferences(Base):
    __tablename__ = "form_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    answer_id = Column(DateTime, nullable=False)
    topic_1 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic_2 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    topic_3 = Column(
        Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    student = relationship("User", lazy="noload", cascade="all, delete")
    topic_1_rel = relationship("Topic", foreign_keys=[topic_1])
    topic_2_rel = relationship("Topic", foreign_keys=[topic_2])
    topic_3_rel = relationship("Topic", foreign_keys=[topic_3])
