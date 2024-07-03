from api.models import TopicCategoryItem, TopicItem
from api.services.topic_service import TopicService


class TopicController:

    def __init__(self, service: TopicService):
        self._service = service

    def _format_item(self, item):
        return {"name": item.name}

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            new_item = self._service.add_topic_category(topic_category)
            return self._format_item(new_item)
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicItem):
        try:
            return topic
        except Exception as err:
            raise err
