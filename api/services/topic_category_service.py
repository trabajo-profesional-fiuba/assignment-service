from api.models import TopicCategoryItem
from api.repositories.topic_category_repository import TopicCategoryRepository


class TopicCategoryService:

    def __init__(self, repository: TopicCategoryRepository):
        self._repository = repository

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            return self._repository.add_topic_category(topic_category)
        except Exception as err:
            raise err
