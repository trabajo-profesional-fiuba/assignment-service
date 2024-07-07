from api.models import (
    TopicCategoryItem,
    TopicItem,
    TopicPreferencesItem,
    TopicPreferencesUpdatedItem,
)
from storage.tables import TopicCategory, Topic, TopicPreferences
from sqlalchemy.exc import IntegrityError


class TopicRepository:

    def __init__(self, db):
        self._db = db

    def get_topic_category_by_name(self, name: str):
        try:
            session = self._db.get_db()
            db_item = (
                session.query(TopicCategory).filter(TopicCategory.name == name).first()
            )
            return db_item
        except Exception as err:
            raise err

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            session = self._db.get_db()
            db_item = TopicCategory(name=topic_category.name)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            raise err

    def add_topic(self, topic):
        try:
            session = self._db.get_db()
            category = self.get_topic_category_by_name(topic.category)
            db_item = Topic(name=topic.name, category=category.id)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            raise err

    def get_topic(self, topic: TopicItem):
        try:
            session = self._db.get_db()
            category = self.get_topic_category_by_name(topic.category)
            db_item = (
                session.query(Topic)
                .filter(Topic.name == topic.name)
                .filter(Topic.category == category.id)
                .first()
            )
            return db_item
        except Exception as err:
            raise err

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
        except IntegrityError:
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
