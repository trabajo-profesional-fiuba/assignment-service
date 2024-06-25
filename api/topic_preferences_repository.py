from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.exceptions import TopicPreferencesDuplicated, StudentNotFound
from sqlalchemy.exc import IntegrityError
from storage.topic_preferences_table import TopicPreferences


class TopicPreferencesRepository:

    def __init__(self, db):
        self._db = db

    def add_topic_preferences(
        self, email: str, topic_preferences: TopicPreferencesItem
    ):
        try:
            session = self._db.get_db()
            db_item = TopicPreferences(
                email=email,
                group_id=topic_preferences.group_id,
                topic1=topic_preferences.topic1,
                topic2=topic_preferences.topic2,
                topic3=topic_preferences.topic3,
            )
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except IntegrityError as err:
            if email == topic_preferences.email:
                session.rollback()
                raise TopicPreferencesDuplicated(topic_preferences.email)
            else:
                return db_item

    def update_topic_preferences(
        self, email: str, topic_preferences_update: TopicPreferencesUpdatedItem
    ):
        try:
            session = self._db.get_db()
            db_item = (
                session.query(TopicPreferences)
                .filter(TopicPreferences.email == email)
                .first()
            )

            if db_item is None:
                raise StudentNotFound(email)

            update_data = topic_preferences_update.model_dump()
            for field, value in update_data.items():
                setattr(db_item, field, value)

            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            session.rollback()
            raise err
