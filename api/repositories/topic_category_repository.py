from api.models import TopicCategoryItem
from storage.tables import TopicCategory


class TopicCategoryRepository:

    def __init__(self, db):
        self._db = db

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
