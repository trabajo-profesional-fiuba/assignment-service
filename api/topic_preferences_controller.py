from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem


class TopicPreferenceController:

    def __init__(self, service):
        self._service = service

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

    def update_topic_preferences(
        self,
        email_sender: str,
        topic_preferences_update: TopicPreferencesUpdatedItem,
    ):
        try:
            updated_items = self._service.update_topic_preferences(
                email_sender, topic_preferences_update
            )
            formatted_items = self._format_items(updated_items)
            return formatted_items
        except Exception as err:
            raise err
