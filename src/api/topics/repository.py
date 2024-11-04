from sqlalchemy.orm import Session

from src.api.topics.exceptions import CategoryNotFound, TopicNotFound
from src.api.topics.models import Category, Topic, TopicTutorPeriod
from src.api.tutors.models import TutorPeriod


class TopicRepository:

    def __init__(self, sess: Session):
        self.Session = sess

    def add_categories(self, categories: list[Category]):
        """Agrega una lista de Categorias a la tabla"""
        categories_saved = list()
        with self.Session() as session:
            for category in categories:
                exists = (
                    session.query(Category)
                    .filter(Category.name == category.name)
                    .first()
                )
                if not exists:
                    session.add(category)
                    session.commit()
                    session.refresh(category)
                    categories_saved.append(category)

                else:
                    categories_saved.append(exists)
            session.expunge_all()
        return categories_saved

    def add_topics(self, topics: list[Topic]):
        """Agrega una lista de temas a la tabla"""
        topics_saved = list()
        with self.Session() as session:
            for topic in topics:
                topic_db = session.query(Topic).filter(Topic.name == topic.name).first()
                if topic_db:
                    session.expunge(topic_db)
                    topics_saved.append(topic_db)
                else:
                    session.add(topic)
                    session.commit()
                    session.refresh(topic)
                    session.expunge(topic)
                    topics_saved.append(topic)

        return topics_saved

    def add_topic_with_category(self, topic: Topic, category_name: str):
        """Agrega un tema y su categoria asociada"""
        with self.Session() as session:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                raise CategoryNotFound(
                    f"Category with name: {category_name} is not in db"
                )

            topic.category_id = category.id
            session.add(topic)
            session.commit()
            session.refresh(topic)
            session.expunge(topic)

        return topic

    def get_topics(self):
        """Devuelve todos los temas"""
        with self.Session() as session:
            topics = session.query(Topic).all()
            session.expunge_all()
        return topics

    def get_categories(self):
        """Devuelve todos las categorias"""

        with self.Session() as session:
            categories = session.query(Category).all()
            session.expunge_all()

        return categories

    def add_category(self, category: Category):
        """Agrega una categoria"""
        with self.Session() as session:
            session.add(category)
            session.commit()
            session.refresh(category)
            session.expunge(category)
        return category

    def add_topic(self, topic: Topic):
        """Agrega un tema"""
        with self.Session() as session:
            session.add(topic)
            session.commit()
            session.refresh(topic)
            # force loading the category
            topic.category
            session.expunge(topic)
        return topic

    def get_topic_by_name(self, name: str):
        """Devuelve tema a partir del nombre"""
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.name == name).first()
            if topic:
                session.expunge(topic)
        return topic

    def get_topic_by_id(self, id: int):
        """Devuelve tema por id"""
        with self.Session() as session:
            topic = session.query(Topic).filter(Topic.id == id).first()
            session.expunge_all()
        return topic

    def get_topics_by_period_id(self, period_id):
        """Devuelve todas las categorias de un cuatrimestre particular"""
        with self.Session() as session:
            topics = (
                session.query(Topic)
                .join(TopicTutorPeriod)
                .join(TutorPeriod)
                .filter(TutorPeriod.period_id == period_id)
                .all()
            )
            session.expunge_all()

        return topics

    def delete_topic(self, topic_id):
        with self.Session() as session:
            topic_to_delete = (
                session.query(Topic).filter(Topic.id == topic_id).one_or_none()
            )

            if topic_to_delete is None:
                raise TopicNotFound(f"Topic {topic_id} not found")

            session.delete(topic_to_delete)
            session.commit()
            return topic_to_delete
