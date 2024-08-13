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

    def add_category(self, category: Category):
        with self.Session() as session:
            session.add(category)
            session.commit()
            session.refresh(category)
            session.expunge(category)
        return category

    def add_topic(self, topic: Topic):
        with self.Session() as session:
            session.add(topic)
            session.commit()
            session.refresh(topic)
            session.expunge(topic)
        return topic

    def get_topic_by_name(self, name: str):
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.name == name).first()
            if topic:
                session.expunge(topic)
        return topic
