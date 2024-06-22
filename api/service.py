from api.models import TopicPreferencesItem
from api.repository import Repository


class TopicTutorService:
    def __init__(self, repository: Repository):
        self._repository = repository

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        self._repository.add_topic_preferences(topic_preferences)
        return topic_preferences

    def update_topic_preferences(
        self, email, topic_preferences_update: TopicPreferencesItem
    ):
        self._repository.update_topic_preferences(email, topic_preferences_update)
        return topic_preferences_update
