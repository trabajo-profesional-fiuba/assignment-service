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

    def _format_topics(self, session, topics: list[Topic]):
        topics_to_add = []
        for topic_request in topics:
            category = (
                session.query(Category).filter_by(name=topic_request.category).first()
            )
            topic = Topic(name=topic_request.name, category=category.id)
            topics_to_add.append(topic)

        return topics_to_add

    def add_topics(self, topics: list[Topic]):
        with self.Session() as session:
            formatted_topics = self._format_topics(session, topics)
            session.add_all(formatted_topics)
            session.commit()

            for topic in formatted_topics:
                session.refresh(topic)
                topic.topic_category
                session.expunge(topic)

            return formatted_topics

    def get_topics(self):
        with self.Session() as session:
            topics = session.query(Topic).all()

            for topic in topics:
                topic.topic_category
                session.expunge(topic)

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

    def get_topic_by_id(self, id: int):
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.id == id).first()
            if topic:
                session.expunge(topic)
        return topic

    def delete_topics(self):
        with self.Session() as session:
            session.query(Category).delete()
            session.query(Topic).delete()
            session.commit()
