from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from storage.tables import TopicPreferences
from api.exceptions import TopicPreferencesNotFound
from sqlalchemy.exc import IntegrityError


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
                topic_1=topic_preferences.topic_1,
                topic_2=topic_preferences.topic_2,
                topic_3=topic_preferences.topic_3,
            )
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except IntegrityError as err:
            db_item = self.update_topic_preferences(email, topic_preferences)
            return db_item
        except Exception as err:
            session.rollback()
            raise err

    def get_topic_preferences_by_email(self, email: str):
        try:
            session = self._db.get_db()
            db_item = (
                session.query(TopicPreferences)
                .filter(TopicPreferences.email == email)
                .first()
            )
            return db_item
        except Exception as err:
            session.rollback()
            raise err

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

            update_data = topic_preferences_update.model_dump()
            for field, value in update_data.items():
                setattr(db_item, field, value)

            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            session.rollback()
            raise err
