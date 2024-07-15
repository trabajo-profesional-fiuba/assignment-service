from src.api.topic.schemas import (
    TopicCategoryRequest,
    TopicRequest,
    TopicPreferencesRequest,
)
from src.api.topic.repository import TopicRepository
from src.api.topic.exceptions import (
    TopicCategoryDuplicated,
    TopicDuplicated,
    UidDuplicated,
)


class TopicService:

    def __init__(self, topic_repository: TopicRepository):
        self._repository = topic_repository

    def add_topic_category_if_not_duplicated(
        self, topic_category: TopicCategoryRequest
    ):
        """
        Adds a topic category if it does not already exists.
        Raises a 'TopicCategoryDuplicated' exception otherwise.
        """
        try:
            if self._repository.get_topic_category_by_name(topic_category.name) is None:
                return self._repository.add_topic_category(topic_category)
            raise TopicCategoryDuplicated()
        except Exception as err:
            raise err

    def add_topic_category(self, topic_category: TopicCategoryRequest):
        """
        Adds a topic category.
        """
        try:
            return self.add_topic_category_if_not_duplicated(topic_category)
        except Exception as err:
            raise err

    def add_topic_if_not_duplicated(self, topic: TopicRequest):
        """
        Adds a topic if it does not already exists.
        Raise a 'TopicDuplicated' exception otherwise.
        """
        try:
            if (
                self._repository.get_topic_by_name_and_category(
                    topic.name, topic.category
                )
                is None
            ):
                self._repository.add_topic(topic)
                return topic
            raise TopicDuplicated()
        except Exception as err:
            raise err

    def add_topic(self, topic: TopicRequest):
        """
        Adds a topic.
        """
        try:
            return self.add_topic_if_not_duplicated(topic)
        except Exception as err:
            raise err

    def add_all_topic_preferences(
        self, student_emails: list, topic_preferences: TopicPreferencesRequest
    ):
        """
        Adds a topic preference for each student of the group if it does not already exists.
        Raises a 'UidDuplicated' exception otherwise.
        """
        try:
            created = []
            for email in student_emails:
                if self._repository.get_topic_preferences_by_uid(email) is None:
                    created.append(
                        self._repository.add_topic_preferences(email, topic_preferences)
                    )
                else:
                    raise UidDuplicated(email)
            return created
        except Exception as err:
            raise err

    def filter_student_uids(self, student_uids: list):
        """
        Returns not none students university ids.
        """
        filtered = []
        for email in student_uids:
            if email is not None:
                filtered.append(email)
        return filtered

    def add_topic_preferences(self, topic_preferences: TopicPreferencesRequest):
        """
        Adds a topic preferences for every student in the group.
        Returns created topic preferences.
        """
        try:
            return self.add_all_topic_preferences(
                self.filter_student_uids(
                    [
                        topic_preferences.uid_sender,
                        topic_preferences.uid_student_2,
                        topic_preferences.uid_student_3,
                        topic_preferences.uid_student_4,
                    ]
                ),
                topic_preferences,
            )
        except Exception as err:
            raise err
