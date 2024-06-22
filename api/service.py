from api.models import TopicPreferencesItem
from api.repository import Repository


class TopicTutorService:
    def __init__(self, repository: Repository):
        self._repository = repository

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        response = self._repository.add_topic_preferences(topic_preferences)
        return response
