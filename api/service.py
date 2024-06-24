from api.models import TopicPreferencesItem, TopicPreferencesUpdatedItem
from api.repository import Repository
from api.exceptions import TopicPreferencesDuplicated
from typing import Union


class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    def add_items(self, emails: list, item: TopicPreferencesItem):
        created_items = []
        for email in emails:
            if email:
                created_items.append(
                    self._repository.add_topic_preferences(email, item)
                )
        return created_items

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            new_items = self.add_items(
                [
                    topic_preferences.email,
                    topic_preferences.email_student_group_2,
                    topic_preferences.email_student_group_3,
                    topic_preferences.email_student_group_4,
                ],
                topic_preferences,
            )
            return new_items
        except Exception as err:
            raise err

    def update_items(self, emails: list, item: TopicPreferencesUpdatedItem):
        updated_items = []
        for email in emails:
            if email:
                updated_items.append(
                    self._repository.update_topic_preferences(email, item)
                )
        return updated_items

    def update_topic_preferences(
        self, email: str, topic_preferences_update: TopicPreferencesUpdatedItem
    ):
        try:
            updated_items = self.update_items(
                [
                    email,
                    topic_preferences_update.email_student_group_2,
                    topic_preferences_update.email_student_group_3,
                    topic_preferences_update.email_student_group_4,
                ],
                topic_preferences_update,
            )
            return updated_items
        except Exception as err:
            raise err
