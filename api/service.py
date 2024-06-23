from api.models import TopicPreferencesItem
from api.repository import Repository
from api.exceptions import TopicPreferencesDuplicated


class TopicTutorService:
    def __init__(self, repository: Repository):
        self._repository = repository

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            self._repository.add_topic_preferences(topic_preferences)
            return topic_preferences
        except TopicPreferencesDuplicated as e:
            print(f"[Service]: {e}")
            raise e

    def update_topic_preferences(
        self, email, topic_preferences_update: TopicPreferencesItem
    ):
        self._repository.update_topic_preferences(email, topic_preferences_update)
        return topic_preferences_update
