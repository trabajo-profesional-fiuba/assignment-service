from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.auth.hasher import ShaHasher
from src.api.topic.exceptions import TopicAlreadyExist


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def add_category(self, category_name: str, categories: list[CategoryRequest]):
        new_category = CategoryRequest(name=category_name)
        if not any(category.name == category_name for category in categories):
            categories.append(new_category)
        return categories

    def add_topic(
        self, topic_name: str, category_name: str, topics: list[TopicRequest]
    ):
        new_topic = TopicRequest(name=topic_name, category=category_name)
        if not any(topic.name == topic_name for topic in topics):
            topics.append(new_topic)
            return topics
        raise TopicAlreadyExist("Topic already exists.")

    def get_categories_topics(self, rows):
        try:
            categories = []
            topics = []
            for i in rows:
                name, category = i
                categories = self.add_category(category, categories)
                topics = self.add_topic(name, category, topics)
            return categories, topics
        except Exception as err:
            raise err

    def create_topics_from_string(self, csv: str, hasher: ShaHasher):
        try:
            csv_file = TopicCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            categories, topics = self.get_categories_topics(rows)
            self._repository.add_categories(categories)
            return self._repository.add_topics(topics)
        except Exception as err:
            raise err
