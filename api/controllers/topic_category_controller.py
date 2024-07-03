from api.models import TopicCategoryItem
from api.services.topic_category_service import TopicCategoryService


class TopicCategoryController:

    def __init__(self, service: TopicCategoryService):
        self._service = service

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            return self._service.add_topic_category(topic_category)
        except Exception as err:
            raise err
