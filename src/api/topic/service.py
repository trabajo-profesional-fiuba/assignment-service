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

    def add_topic_category(self, topic_category: TopicCategoryItem):
        try:
            if (
                self._topic_repository.get_topic_category_by_name(topic_category.name)
                is None
            ):
                return self._topic_repository.add_topic_category(topic_category)
            raise TopicCategoryDuplicated()
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicItem):
        try:
            category = self._topic_repository.get_topic_category_by_name(topic.category)
            if category is not None:
                if self._topic_repository.get_topic(topic) is None:
                    self._topic_repository.add_topic(topic)
                    return topic
                raise TopicDuplicated()
            raise TopicCategoryNotFound()
        except Exception as err:
            raise err

    def add_items(self, emails: list, item: TopicPreferencesItem):
        try:
            print("add_items service {item} {emails}")
            created_items = []
            for email in emails:
                print("email: ", email)
                if email is not None:
                    created_items.append(
                        self._topic_repository.add_topic_preferences(email, item)
                    )
            print("created items: ", created_items)
            return created_items
        except Exception as err:
            raise err

    def add_topic_preferences(self, topic_preferences: TopicPreferencesItem):
        try:
            print("add_topic_preferences service: ", topic_preferences)
            new_items = self.add_items(
                [
                    topic_preferences.email_sender,
                    topic_preferences.email_student_2,
                    topic_preferences.email_student_3,
                    topic_preferences.email_student_4,
                ],
                topic_preferences,
            )
            print("new items", new_items)
            return new_items
        except Exception as err:
            raise err
