from src.api.topic.schemas import (
    TopicCategoryRequest,
    TopicRequest,
    TopicPreferencesRequest,
)
from src.api.topic.service import TopicService


class TopicController:

    def __init__(self, service: TopicService):
        self._service = service

    def _format_topic_category(self, item):
        return {"name": item.name}

    def add_topic_category(self, topic_category: TopicCategoryRequest):
        try:
            new_item = self._service.add_topic_category(topic_category)
            return self._format_topic_category(new_item)
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        try:
            return self._service.add_topic(topic)
        except Exception as err:
            raise err

    def _format_topic_preferences(
        self, new_items: list, request: TopicPreferencesRequest
    ):
        """
        Deletes other students from the same group email.
        """
        formatted_list = []
        for new_item in new_items:
            formatted_item = {
                "email": new_item.email,
                "group_id": new_item.group_id,
                "topic_1": request.topic_1,
                "category_1": request.category_1,
                "topic_2": request.topic_2,
                "category_2": request.category_2,
                "topic_3": request.topic_3,
                "category_3": request.category_3,
            }
            formatted_list.append(formatted_item)
        return formatted_list

    def add_topic_preferences(self, topic_preferences: TopicPreferencesRequest):
        try:
            new_items = self._service.add_topic_preferences(topic_preferences)
            return self._format_topic_preferences(new_items, topic_preferences)
        except Exception as err:
            raise err
