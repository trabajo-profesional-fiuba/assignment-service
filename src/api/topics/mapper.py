from typing import Optional
from src.core.topic import Topic
from src.api.topics.models import Topic as TopicModel


class TopicMapper:

    def map_models_to_topics(self, db_topics: list[TopicModel]):
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

    def map_model_to_topic(self, topic: Optional[TopicModel] = None):
        if topic:
            return Topic(id=topic.id, title=topic.name, category=topic.category.name)
