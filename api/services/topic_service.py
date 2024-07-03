from api.models import TopicCategoryItem, TopicItem
from api.repositories.topic_repository import TopicRepository
from api.exceptions import TopicCategoryDuplicated


class TopicService:

    def __init__(self, repository: TopicRepository):
        self._repository = repository

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            if self._repository.get_topic_category_by_name(topic_category.name) is None:
                return self._repository.add_topic_category(topic_category)
            raise TopicCategoryDuplicated()
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicItem):
        try:
            return topic
        except Exception as err:
            raise err
