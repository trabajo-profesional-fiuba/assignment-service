from src.core.topic import Topic


class TopicMapper:

    def convert_from_models_to_topic(self, db_topics):
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
