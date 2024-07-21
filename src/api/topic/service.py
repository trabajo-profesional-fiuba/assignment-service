from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.utils import TopicCsvFile
from src.api.auth.hasher import ShaHasher


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def get_categories_topics(self, rows):
        categories = []
        topics = []
        for i in rows:
            name, category = i
            categories.append(CategoryRequest(name=category))
            topics.append(TopicRequest(name=name, category=category))
        return categories, topics

    def create_topics_from_string(self, csv: str, hasher: ShaHasher):
        try:
            csv_file = TopicCsvFile(csv=csv)
            rows = csv_file.get_info_as_rows()
            categories, topics = self.get_categories_topics(rows)
            self._repository.add_categories(categories)
            return self._repository.add_topics(topics)
        except Exception as err:
            raise err
