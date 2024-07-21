from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import psycopg2

from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicResponse,
)
from src.api.topic.models import Category, Topic
from src.api.topic.exceptions import (
    CategoryAlreadyExist,
    CategoryNotFound,
    TopicAlreadyExist,
)


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_category(self, category: CategoryRequest):
        try:
            with self.Session() as session:
                with session.begin():
                    db_item = Category(name=category.name)
                    session.add(db_item)
                    return CategoryResponse.from_orm(db_item)
        except IntegrityError:
            raise CategoryAlreadyExist(f"Category '{category.name}' already exists.")
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        try:
            with self.Session() as session:
                with session.begin():
                    db_item = Topic(name=topic.name, category=topic.category)
                    session.add(db_item)
                    return TopicResponse.from_orm(db_item)
        except Exception as err:
            raise CategoryNotFound(f"Category '{topic.category}' not found.")
