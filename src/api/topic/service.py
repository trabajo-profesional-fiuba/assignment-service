from src.api.topic.schemas import (
    CategoryRequest,
    TopicRequest,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.exceptions import (
    CategoryDuplicated,
    TopicDuplicated,
    UidDuplicated,
)


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def add_category(self, category: CategoryRequest):
        try:
            return self._repository.add_category(category)
        except CategoryDuplicated as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        """
        Adds a topic.
        """
        try:
            return self._repository.add_topic(topic)
        except Exception as err:
            raise err

    def get_categories(self):
        try:
            return self._repository.get_categories()
        except Exception as err:
            raise err
