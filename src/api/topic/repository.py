from sqlalchemy.orm import Session

from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
    TopicPreferencesRequest,
)
from src.api.topic.models import TopicCategory, Topic, TopicPreferences
from src.api.topic.exceptions import TopicCategoryNotFound, TopicNotFound, InsertTopicException


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess


    def add_category(self, category: CategoryRequest):
        try:
            with self.Session() as session:
                db_item = TopicCategory(name=category.name)
                session.add(session)
                session.commit()
                return db_item
        except Exception as err:
            raise err

    
    def get_category_by_name(self, name: str):
        try:
            with self.Session() as session:
                db_item = session.query(TopicCategory).filter(TopicCategory.name == name).scalar()  
                return db_item
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        try:
            with self.Session() as session:
                category = session.query(TopicCategory).filter(TopicCategory.name == topic.category).scalar()
                if not category:
                    raise TopicCategoryNotFound(f"{topic.category} does not exist in the database")
                db_item = Topic(name=topic.name, category_id=category.id)
                session.add(db_item)
                session.commit()
                return db_item
        except Exception as _:
            raise InsertTopicException(f"{topic.__str__} coud not be inserted into db")

    def get_topic_by_name_and_category(self, name: str, category: str):
        try:
            with self.Session() as session:
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
