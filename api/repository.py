from api.database import TopicPreferences
from api.models import TopicPreferencesItem


class Repository:

    def __init__(self, db):
        self._db = db

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
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
            return db_item
        except Exception as e:
            self._db.rollback()
            print(f"An error occurred: {e}")
        finally:
            self._db.close()

    def update_topic_preferences(
        self, email: str, topic_preferences_update: TopicPreferencesItem
    ):
        db_item = (
            self._db.query(TopicPreferences)
            .filter(TopicPreferences.email == email)
            .first()
        )
        for field, value in topic_preferences_update.dict(exclude_unset=True).items():
            setattr(db_item, field, value)
        self._db.commit()
        self._db.refresh(db_item)
        return db_item
