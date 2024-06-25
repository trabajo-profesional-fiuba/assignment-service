from sqlalchemy import Column, String, DateTime, Table
from storage.database import Base


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"
    __table__ = Table(
        "topic_preferences",
        Base.metadata,
        Column("email", String, primary_key=True, index=True),
        Column("group_id", DateTime),
        Column("topic1", String),
        Column("topic2", String),
        Column("topic3", String),
        extend_existing=True,  # This will prevent redefinition errors
    )
