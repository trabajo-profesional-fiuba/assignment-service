from src.api.topic.schemas import TopicCategoryItem, TopicItem, TopicPreferencesItem
from src.api.topic.models import TopicCategory, Topic, TopicPreferences
from src.api.topic.exceptions import TopicCategoryNotFound, TopicNotFound


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
            if not category:
                raise TopicCategoryNotFound(topic.category)
            db_item = Topic(name=topic.name, category=category.id)
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            raise err

    def get_topic_by_name_and_category(self, name: str, category: str):
        try:
            session = self._db.get_db()
            category_item = self.get_topic_category_by_name(category)
            if not category_item:
                raise TopicCategoryNotFound(category)
            db_item = (
                session.query(Topic)
                .filter(Topic.name == name)
                .filter(Topic.category == category_item.id)
                .first()
            )
            return db_item
        except Exception as err:
            raise err

    def delete_topic_preferences(self, email: str):
        try:
            session = self._db.get_db()
            db_item = (
                session.query(TopicPreferences)
                .filter(TopicPreferences.email == email)
                .first()
            )
            session.delete(db_item)
            session.commit()
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

    def add_topic_preferences(
        self, email: str, topic_preferences: TopicPreferencesItem
    ):
        try:
            session = self._db.get_db()

            topic_1 = self.get_topic_by_name_and_category(
                topic_preferences.topic_1, topic_preferences.category_1
            )
            if not topic_1:
                raise TopicNotFound(
                    topic_preferences.topic_1, topic_preferences.category_1
                )
            topic_2 = self.get_topic_by_name_and_category(
                topic_preferences.topic_2, topic_preferences.category_2
            )
            if not topic_2:
                raise TopicNotFound(
                    topic_preferences.topic_2, topic_preferences.category_2
                )
            topic_3 = self.get_topic_by_name_and_category(
                topic_preferences.topic_3, topic_preferences.category_3
            )
            if not topic_3:
                raise TopicNotFound(
                    topic_preferences.topic_3, topic_preferences.category_3
                )

            db_item = TopicPreferences(
                email=email,
                group_id=topic_preferences.group_id,
                topic_1=topic_1.id,
                topic_2=topic_2.id,
                topic_3=topic_3.id,
            )
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            session.rollback()
            raise err
