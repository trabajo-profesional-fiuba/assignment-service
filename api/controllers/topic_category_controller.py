from api.models import TopicCategoryItem
from api.services.topic_category_service import TopicCategoryService


class TopicCategoryController:

    def __init__(self, service: TopicCategoryService):
        self._service = service

    def _format_item(self, item):
        return {"name": item.name}

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            new_item = self._service.add_topic_category(topic_category)
            return self._format_item(new_item)
        except Exception as err:
            raise err
