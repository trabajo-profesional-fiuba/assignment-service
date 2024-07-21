from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.api.topic.schemas import (
    CategoryRequest,
    CategoryResponse,
    TopicRequest,
    TopicResponse,
)
from src.api.topic.models import Category, Topic
from src.api.topic.exceptions import (
    CategoryNotFound,
    CategoryAlreadyExist,
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
            raise CategoryAlreadyExist()
        except Exception as err:
            raise err

    def get_category_by_name(self, name: str):
        try:
            with self.Session() as session:
                db_item = session.query(Category).filter(Category.name == name).scalar()
                return db_item
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        try:
            with self.Session() as session:
                category = (
                    session.query(Category)
                    .filter(Category.name == topic.category)
                    .scalar()
                )
                if not category:
                    raise CategoryNotFound(
                        f"{topic.category} does not exist in the database"
                    )
                db_item = Topic(name=topic.name, category=category.name)
                session.add(db_item)
                session.commit()
                return TopicResponse.from_orm(db_item)
        except Exception as err:
            raise err
