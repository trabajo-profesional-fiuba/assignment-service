from src.core.topic import Topic
from src.api.topics.models import Topic as TopicModel


class TopicMapper:

    def convert_from_models_to_topic(self, db_topics: list[TopicModel]):
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
