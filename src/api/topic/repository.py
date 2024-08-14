from sqlalchemy.orm import Session
from src.api.topic.models import Category, Topic


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

    """ Add a list of topics and detached them from the session"""

    def add_topics(self, topics: list[Topic]):
        with self.Session() as session:
            session.add_all(topics)
            session.commit()
            for topic in topics:
                session.refresh(topic)
                session.expunge(topic)
        return topics

    """ Get all the topics"""

    def get_topics(self):
        with self.Session() as session:
            topics = session.query(Topic).all()
            session.expunge_all()
        return topics

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
            session.expunge(topic)
        return topic

    """ Get a topic based on the name and detached it from the session"""

    def get_topic_by_name(self, name: str):
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.name == name).first()
            if topic:
                session.expunge(topic)
        return topic
