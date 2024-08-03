from sqlalchemy.orm import Session
from src.api.topic.models import Category, Topic


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

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
                session.expunge(topic)
        return topics

    def get_topics(self):
        with self.Session() as session:
            topics = session.query(Topic).all()
            session.expunge_all()
        return topics
