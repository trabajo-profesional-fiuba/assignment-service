from api.models import TopicCategoryItem, TopicItem, TopicPreferencesItem
from storage.tables import TopicCategory, Topic, TopicPreferences


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

    def get_topic_by_name_and_category(self, topic_name: str, topic_category: str):
        try:
            session = self._db.get_db()
            category = self.get_topic_category_by_name(topic_category)
            db_item = (
                session.query(Topic)
                .filter(Topic.name == topic_name)
                .filter(Topic.category == category.id)
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
            if db_item:
                session.delete(db_item)
                session.commit()
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
            ).id
            topic_2 = self.get_topic_by_name_and_category(
                topic_preferences.topic_2, topic_preferences.category_2
            ).id
            topic_3 = self.get_topic_by_name_and_category(
                topic_preferences.topic_3, topic_preferences.category_3
            ).id

            db_item = TopicPreferences(
                email=email,
                group_id=topic_preferences.group_id,
                topic_1=topic_1,
                topic_2=topic_2,
                topic_3=topic_3,
            )
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return db_item
        except Exception as err:
            session.rollback()
            raise err
