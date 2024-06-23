from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.repository import Repository
from api.exceptions import TopicPreferencesDuplicated


class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            item_1 = self._repository.add_topic_preferences(
                topic_preferences.email, topic_preferences
            )
            item_2 = self._repository.add_topic_preferences(
                topic_preferences.email_student_group_2, topic_preferences
            )
            item_3 = self._repository.add_topic_preferences(
                topic_preferences.email_student_group_3, topic_preferences
            )
            item_4 = self._repository.add_topic_preferences(
                topic_preferences.email_student_group_4, topic_preferences
            )
            return [item_1, item_2, item_3, item_4]
        except TopicPreferencesDuplicated as err:
            raise err

    def delete_other_students_email(self, items: list):
        dict_items = []
        for item in items:
            dict_item = {
                "email": item.email,
                "group_id": item.group_id,
                "topic1": item.topic1,
                "topic2": item.topic2,
                "topic3": item.topic3,
            }
            dict_items.append(dict_item)
        return dict_items

    def update_topic_preferences(
        self, email: str, topic_preferences_update: TopicPreferencesUpdatedItem
    ):
        item_1 = self._repository.update_topic_preferences(
            email, topic_preferences_update
        )
        item_2 = self._repository.update_topic_preferences(
            topic_preferences_update.email_student_group_2, topic_preferences_update
        )
        item_3 = self._repository.update_topic_preferences(
            topic_preferences_update.email_student_group_3, topic_preferences_update
        )
        item_4 = self._repository.update_topic_preferences(
            topic_preferences_update.email_student_group_4, topic_preferences_update
        )
        items = self.delete_other_students_email([item_1, item_2, item_3, item_4])
        return items
