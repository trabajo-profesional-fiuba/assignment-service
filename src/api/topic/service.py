from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
    TopicList,
    TopicResponse,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.topic.exceptions import TopicAlreadyExist
from src.api.topic.models import Topic, Category

from src.config.logging import logger 


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def _add_category(self, category_name: str, categories: list[Category]):
        new_category = Category(name=category_name)
        if not any(category.name == category_name for category in categories):
            categories.append(new_category)
        return categories

    def _add_topic(self, topic_name: str, category_name: str, topics: list[Topic]):
        new_topic = Topic(name=topic_name, category=category_name)
        if not any(topic.name == topic_name for topic in topics):
            topics.append(new_topic)
            return topics
        raise TopicAlreadyExist("Topic already exists.")

    def add_topic(self, topic_name: str):
        topic = Topic(name=topic_name, category="default")
        return TopicResponse.model_validate(self._repository.add_topic(topic))

    def get_or_add_topic(self, topic_name: str):
        """
        Atempts to retrieve the topic from the database
        if the topic is not in db, it creates it with a 
        default category
        """
        topic_db = self._repository.get_topic_by_name(topic_name)
        if not topic_db:
            logger.info(f"Topic name {topic_name} is not in db, adding it with default category")
            topic_db = self._repository.add_topic(
                Topic(name=topic_name, category="default")
            )
        return TopicResponse.model_validate(topic_db)

    def get_categories_topics(self, rows):
        """
        Processes a list of rows containing topic names and categories, and returns
        two lists: one of unique categories and another of unique topics with their
        respective categories.
        """
        categories = []
        topics = []
        for row in rows:
            name, category = row
            categories = self._add_category(category, categories)
            topics = self._add_topic(name, category, topics)
        return categories, topics

    def create_topics_from_string(self, csv: str):
        csv_file = TopicCsvFile(csv=csv)
        rows = csv_file.get_info_as_rows()
        categories, topics = self.get_categories_topics(rows)
        self._repository.add_categories(categories)
        return TopicList.model_validate(self._repository.add_topics(topics))

    def get_topics(self):
        topics = self._repository.get_topics()
        return TopicList.model_validate(topics)
