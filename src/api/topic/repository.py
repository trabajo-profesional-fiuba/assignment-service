from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicResponse,
)
from src.api.topic.models import Category, Topic
from src.api.topic.exceptions import CategoryAlreadyExist, CategoryNotFound


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_categories(self, categories: list[CategoryRequest]):
        try:
            with self.Session() as session:
                with session.begin():
                    db_items = []
                    response = []
                    for category in categories:
                        db_item = Category(name=category.name)
                        db_items.append(db_item)
                        response.append(CategoryResponse.from_orm(db_item))
                    session.add_all(db_items)
                    return response
        except IntegrityError:
            raise CategoryAlreadyExist(f"Category '{category.name}' already exists.")
        except Exception as err:
            raise err

    def add_topics(self, topics: list[TopicRequest]):
        try:
            with self.Session() as session:
                with session.begin():
                    db_items = []
                    response = []
                    for topic in topics:
                        db_item = Topic(name=topic.name, category=topic.category)
                        db_items.append(db_item)
                        response.append(TopicResponse.from_orm(db_item))
                    session.add_all(db_items)
                    return response
        except Exception:
            raise CategoryNotFound(f"Category '{topic.category}' not found.")
