from api.models import (
    TopicCategoryItem,
    TopicItem,
    TopicPreferencesItem,
)
from api.services.topic_service import TopicService


class TopicController:

    def __init__(self, service: TopicService):
        self._service = service

    def _format_topic_category(self, item):
        return {"name": item.name}

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            new_item = self._service.add_topic_category(topic_category)
            return self._format_topic_category(new_item)
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicItem):
        try:
            return self._service.add_topic(topic)
        except Exception as err:
            raise err

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            new_items = self._service.add_topic_preferences(topic_preferences)
            formatted_items = self._format_items(new_items)
            return formatted_items
        except Exception as err:
            raise err

    def _format_items(self, items: list):
        """
        Deletes other students from the same group email.
        """
        dict_items = []
        for item in items:
            dict_item = {
                "email": item.email,
                "group_id": item.group_id,
                "topic_1": item.topic_1,
                "topic_2": item.topic_2,
                "topic_3": item.topic_3,
            }
            dict_items.append(dict_item)
        return dict_items
