from sqlalchemy.orm import Session
from api.database import SessionLocal, engine, Base, TopicPreferences
from api.models import TopicPreferencesItem


class Repository:

    def __init__(self):
        self._db = next(self._get_db())

    def _get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        db_item = TopicPreferences(
            email=topic_preferences.email,
            group_id=topic_preferences.group_id,
            topic1=topic_preferences.topic1,
            topic2=topic_preferences.topic2,
            topic3=topic_preferences.topic3,
        )
        self._db.add(db_item)
        self._db.commit()
        self._db.refresh(db_item)
        return topic_preferences
