from typing import Optional

from src.api.topics.models import Topic as TopicModel
from src.core.topic import Topic


class TopicMapper:

    @staticmethod
    def map_models_to_topics(db_topics: list[TopicModel]):
        """Mappea una lista de temas desde la bd hacia clases nativas de python"""
        topics = list()

        for db_topic in db_topics:
            topic = Topic(
                id=db_topic.id,
                title=db_topic.name,
                category=db_topic.category.name,
                capacity=1,
            )
            topics.append(topic)

        return topics

    @staticmethod
    def map_model_to_topic(topic: Optional[TopicModel] = None):
        """Mappea un tema desde la bd hacia un tema de python"""
        if topic:
            return Topic(id=topic.id, title=topic.name, category=topic.category.name)
