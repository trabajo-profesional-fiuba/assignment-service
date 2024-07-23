from sqlalchemy.orm import Session

from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicResponse,
)
from src.api.topic.models import Category, Topic


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_categories(self, categories: list[CategoryRequest]):
        with self.Session() as session:
            with session.begin():
                db_items = []
                response = []
                for category in categories:
                    db_item = Category(name=category.name)
                    db_items.append(db_item)
                    response.append(CategoryResponse.model_validate(db_item))
                session.add_all(db_items)
                return response

    def add_topics(self, topics: list[TopicRequest]):
        with self.Session() as session:
            with session.begin():
                db_items = []
                response = []
                for topic in topics:
                    db_item = Topic(name=topic.name, category=topic.category)
                    db_items.append(db_item)
                    response.append(TopicResponse.model_validate(db_item))
                session.add_all(db_items)
                return response

    def get_topics(self):
        with self.Session() as session:
            db_items = session.query(Topic).all()
            response = [TopicResponse.model_validate(db_item) for db_item in db_items]
            return response
