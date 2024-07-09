from src.api.topic.schemas import (
    TopicCategoryItem,
    TopicItem,
    TopicPreferencesItem,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.exceptions import (
    TopicCategoryDuplicated,
    TopicCategoryNotFound,
    TopicDuplicated,
)


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._topic_repository = topic_repository

    def add_topic_category_if_not_duplicated(self, topic_category: TopicCategoryItem):
        try:
            if (
                self._topic_repository.get_topic_category_by_name(topic_category.name)
                is None
            ):
                return self._topic_repository.add_topic_category(topic_category)
            raise TopicCategoryDuplicated()
        except Exception as err:
            raise err

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            return self.add_topic_category_if_not_duplicated(topic_category)
        except Exception as err:
            raise err

    def add_topic_if_not_duplicated(
        self, topic: TopicItem, category: TopicCategoryItem
    ):
        try:
            if (
                self._topic_repository.get_topic_by_name_and_category(
                    topic.name, category.name
                )
                is None
            ):
                self._topic_repository.add_topic(topic)
                return topic
            raise TopicDuplicated()
        except Exception as err:
            raise err

    def add_topic_if_category_found(self, topic: TopicItem):
        try:
            category = self._topic_repository.get_topic_category_by_name(topic.category)
            if category is not None:
                return self.add_topic_if_not_duplicated(topic, category)
            raise TopicCategoryNotFound()
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicItem):
        try:
            return self.add_topic_if_category_found(topic)
        except Exception as err:
            raise err

    def add_all_topic_preferences(
        self, student_emails: list, topic_preferences: TopicPreferencesItem
    ):
        try:
            created = []
            for email in student_emails:
                created.append(
                    self._topic_repository.add_topic_preferences(
                        email, topic_preferences
                    )
                )
            return created
        except Exception as err:
            raise err

    def filter_student_emails(self, student_emails: list):
        filtered = []
        for email in student_emails:
            if email is not None:
                filtered.append(email)
        return filtered

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            not_none_emails = self.filter_student_emails(
                [
                    topic_preferences.email_sender,
                    topic_preferences.email_student_2,
                    topic_preferences.email_student_3,
                    topic_preferences.email_student_4,
                ]
            )
            return self.add_all_topic_preferences(
                not_none_emails,
                topic_preferences,
            )
        except Exception as err:
            raise err
