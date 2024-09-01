from sqlalchemy.orm import Session
from src.api.topics.exceptions import CategoryNotFound
from src.api.topics.models import Category, Topic


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    """ Add a list of categories and detached them from the session"""

    def add_categories(self, categories: list[Category]):
        with self.Session() as session:
            session.add_all(categories)
            session.commit()
            for category in categories:
                session.refresh(category)
                session.expunge(category)
        return categories

    def add_topics(self, topics: list[Topic]):
        with self.Session() as session:
            session.add_all(topics)
            session.commit()

            for topic in topics:
                session.refresh(topic)
                topic.category
                session.expunge(topic)

        return topics

    def add_topic_with_category(self, topic: Topic, category_name: str):
        with self.Session() as session:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                raise CategoryNotFound(
                    f"Category with name: {category_name} is not in db"
                )

            topic.category_id = category.id
            session.add(topic)
            session.commit()
            session.expunge(topic)

        return topic

    """ Get all the topics"""

    def get_topics(self):
        with self.Session() as session:
            topics = session.query(Topic).all()

            for topic in topics:
                topic.category
                session.expunge(topic)

        return topics

    """ Get all the categories"""

    def get_categories(self):
        with self.Session() as session:
            categories = session.query(Category).all()
            session.expunge_all()

        return categories

    """ Add a category and detached it from the session"""

    def add_category(self, category: Category):
        with self.Session() as session:
            session.add(category)
            session.commit()
            session.refresh(category)
            session.expunge(category)
        return category

    """ Add a topic and detached it from the session"""

    def add_topic(self, topic: Topic):
        with self.Session() as session:
            session.add(topic)
            session.commit()
            session.refresh(topic)
            # force loading the category
            topic.category
            session.expunge(topic)
        return topic

    """ Get a topic based on the name and detached it from the session"""

    def get_topic_by_name(self, name: str):
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.name == name).first()
            if topic:
                session.expunge(topic)
        return topic

    def get_topic_by_id(self, id: int):
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.id == id).first()
            if topic:
                session.expunge(topic)
        return topic

    def delete_topics(self):
        with self.Session() as session:
            session.query(Category).filter(Category.name != "default").delete()
            session.query(Topic).delete()
            session.commit()
